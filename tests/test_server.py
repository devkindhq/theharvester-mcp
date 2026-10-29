"""MCP stdio JSON-RPC test harness for server.py.

Spawns server.py as a subprocess and speaks Model Context Protocol over
stdin/stdout (JSON-RPC 2.0, newline-delimited).
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

SERVER = Path(__file__).resolve().parent.parent / "server.py"


class McpClient:
    def __init__(self, env_overrides=None):
        env = os.environ.copy()
        env["THEHARVESTER_OUTPUT_DIR"] = str(Path(__file__).parent / "tmp_output")
        if env_overrides:
            env.update(env_overrides)
        self.proc = subprocess.Popen(
            [sys.executable, str(SERVER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1,
        )
        self._id = 0

    def request(self, method, params=None, timeout=20):
        self._id += 1
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params is not None:
            msg["params"] = params
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        deadline = time.time() + timeout
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError(f"server stdout closed: {self.proc.stderr.read()}")
            data = json.loads(line)
            if data.get("id") == self._id:
                return data
            # skip notifications
        raise TimeoutError(f"no response to {method}")

    def notify(self, method, params=None):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def initialize(self):
        resp = self.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pytest-harness", "version": "0.1"},
            },
        )
        self.notify("notifications/initialized")
        return resp

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except Exception:
            self.proc.kill()


@pytest.fixture()
def client():
    c = McpClient()
    c.initialize()
    yield c
    c.close()


def test_initialize_handshake(client):
    # fixture already initialized; verify protocol info came back earlier via fresh client
    c2 = McpClient()
    resp = c2.initialize()
    result = resp["result"]
    assert resp["jsonrpc"] == "2.0"
    assert "serverInfo" in result
    assert result["serverInfo"]["name"] == "theharvester-mcp"
    c2.close()


def test_tools_list_exposes_four_tools(client):
    resp = client.request("tools/list")
    tools = resp["result"]["tools"]
    names = [t["name"] for t in tools]
    assert set(names) == {"harvest", "get_harvest_results", "list_active_harvests", "list_sources"}


def test_list_sources_returns_free_sources(client):
    resp = client.request("tools/call", {"name": "list_sources", "arguments": {}})
    text = resp["result"]["content"][0]["text"]
    data = json.loads(text)
    assert "crtsh" in data["free_sources"]
    assert isinstance(data["all_sources"], list) and len(data["all_sources"]) > 10


def test_list_active_harvests_empty(client):
    resp = client.request("tools/call", {"name": "list_active_harvests", "arguments": {}})
    text = resp["result"]["content"][0]["text"]
    data = json.loads(text)
    assert data == {"active_harvests": []}


def test_harvest_invalid_domain_returns_error_without_spawning(client):
    resp = client.request(
        "tools/call",
        {"name": "harvest", "arguments": {"domain": "not a domain!", "sources": "free", "timeout": 5}},
    )
    text = resp["result"]["content"][0]["text"]
    data = json.loads(text)
    assert data["status"] == "error"
    assert "Invalid domain" in data["error"]

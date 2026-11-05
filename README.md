# theHarvester MCP Server: OSINT email and subdomain discovery for AI agents

theHarvester MCP Server wraps [theHarvester](https://github.com/laramies/theHarvester) in a
[Model Context Protocol](https://modelcontextprotocol.io) server so Claude Code, Cursor, or any
MCP client can harvest public emails, subdomains, hostnames, IPs, and LinkedIn profiles for a
domain on demand. Multi-arch Docker image, stdio transport, no API keys for the default free sources.

It is built for lead generation and prospecting: ask your agent "find public contacts for
example.com" and it calls the `harvest` tool, which fans out to sources like crtsh,
hackertarget, urlscan, and DuckDuckGo, then returns structured JSON. Harvests run asynchronously
with configurable concurrency and timeouts, and results stay retrievable by harvest ID.

## Quick start

```bash
docker pull devkind/theharvester-mcp
```

Add to `.mcp.json` (Claude Code) or your MCP client config:

```json
{
  "mcpServers": {
    "theharvester": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "devkind/theharvester-mcp"]
    }
  }
}
```

Then ask your agent: *"Harvest example.com using free sources."*

### Install in your client

Requirements:

- Docker
- Claude Desktop, Claude Code, Cursor, VS Code, Windsurf, or any other MCP client
- No API keys for the default free sources

**Standard config** works in most MCP clients:

```json
{
  "mcpServers": {
    "theharvester": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "devkind/theharvester-mcp"
      ]
    }
  }
}
```

<details>
<summary>Claude Desktop</summary>

Follow the MCP install [guide](https://modelcontextprotocol.io/quickstart/user) and add the standard config above to your `claude_desktop_config.json`.

</details>

<details>
<summary>Claude Code</summary>

Run:

```bash
claude mcp add theharvester -- docker run --rm -i devkind/theharvester-mcp
```

Or add the standard config above to `.mcp.json` in your project root.

</details>

<details>
<summary>Cursor</summary>

#### Click the button to install:

[<img src="https://cursor.com/deeplink/mcp-install-dark.svg" alt="Install in Cursor">](https://cursor.com/en/install-mcp?name=theHarvester%20MCP&config=eyJjb21tYW5kIjoiZG9ja2VyIiwiYXJncyI6WyJydW4iLCItLXJtIiwiLWkiLCJkZXZraW5kL3RoZWhhcnZlc3Rlci1tY3AiXX0%3D)

#### Or install manually:

Go to `Cursor Settings` -> `MCP` -> `Add new MCP Server`. Name it "theHarvester MCP", use `command` type with the command `docker run --rm -i devkind/theharvester-mcp`.

</details>

<details>
<summary>VS Code</summary>

Follow the MCP install [guide](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server) and use the standard config above. You can also install with the VS Code CLI:

```bash
code --add-mcp '{"name":"theharvester","command":"docker","args":["run","--rm","-i","devkind/theharvester-mcp"]}'
```

</details>

<details>
<summary>Windsurf</summary>

Follow the Windsurf MCP [documentation](https://docs.windsurf.com/windsurf/cascade/mcp) and use the standard config above.

</details>

<details>
<summary>Goose</summary>

Go to `Advanced settings` -> `Extensions` -> `Add custom extension`. Name it "theHarvester MCP", use type `STDIO`, and set the `command` to `docker run --rm -i devkind/theharvester-mcp`. Click "Add Extension".

</details>

<details>
<summary>LM Studio</summary>

Go to `Program` in the right sidebar -> `Install` -> `Edit mcp.json`. Use the standard config above.

</details>

<details>
<summary>Warp</summary>

Go to `Settings` -> `AI` -> `Manage MCP Servers` -> `+ Add` to [add an MCP Server](https://docs.warp.dev/knowledge-and-collaboration/mcp#adding-an-mcp-server). Use the standard config above, or use the slash command `/add-mcp` in the Warp prompt and paste it.

</details>

## Tools

| Tool | What it does |
|---|---|
| `harvest` | Run an OSINT harvest on a domain (sources: `free`, `all`, or comma-separated) |
| `get_harvest_results` | Fetch a previous harvest by ID |
| `list_active_harvests` | Show currently running harvests |
| `list_sources` | List all available sources and which need API keys |

Seven sources work with no API key: crtsh, hackertarget, dnsdumpster, rapiddns, urlscan, otx,
and duckduckgo. Sources like shodan, censys, and virustotal need keys configured in the
theHarvester install.

## Example call and output

Tool call: `harvest` with `{"domain": "example.com", "sources": "free"}`

```json
{
  "harvest_id": "a1b2c3d4",
  "domain": "example.com",
  "status": "completed",
  "duration_seconds": 42.5,
  "sources_used": ["crtsh", "hackertarget", "urlscan"],
  "summary": {"emails": 3, "hosts": 27, "ips": 12, "linkedin": 2},
  "emails": ["info@example.com", "support@example.com", "press@example.com"],
  "hosts": ["www.example.com", "api.example.com", "mail.example.com"]
}
```

Output is illustrative; real counts depend on the target domain and source availability. The
`harvest` tool accepts `domain` (required), `sources` (`free`, `all`, or a comma-separated
list), `limit`, and `timeout`; invalid domains are rejected before any network call.

## Configuration

Environment variables: `THEHARVESTER_TIMEOUT` (default 120s), `THEHARVESTER_MAX_CONCURRENT`
(default 2), `THEHARVESTER_OUTPUT_DIR` (default `/app/output`).

## Responsible use

theHarvester collects only publicly published information, but OSINT tooling attracts scrutiny.
Use this server only on domains you own or have written permission to research, and for lawful
purposes such as security assessment, asset inventory, and business prospecting against public
business contact data. Respect each source's terms of service and applicable privacy and
anti-spam law (GDPR, CAN-SPAM, PECA) when acting on harvested contacts. The maintainers are not
responsible for misuse.

## Roadmap

- [x] Official MCP Registry listing (`io.github.devkindhq/theharvester-mcp`)
- [ ] Docker MCP Registry and Glama listings
- [x] Pinned theHarvester version releases alongside `latest` (`devkind/theharvester-mcp:<version>` is built with theHarvester 4.11.1, `latest` tracks the newest release)
- [x] CI workflow building and pushing the multi-arch image on tag (untested until the first tag)

## License and contributing

[MIT](LICENSE) © Devkind. Issues and PRs welcome, see [CONTRIBUTING.md](CONTRIBUTING.md) and
[SECURITY.md](SECURITY.md).

Built by [Devkind](https://devkind.com.au). Maintained by Kazim Ali.

## Need OSINT and lead generation built into your stack?

Devkind builds custom MCP servers, AI agent workflows and commerce integrations. If you want this kind of harvesting wired into your CRM, enrichment or outreach tooling, [talk to Devkind](https://devkind.com.au/services) or email [hello@devkind.com.au](mailto:hello@devkind.com.au).

# theHarvester MCP Server — OSINT email and subdomain discovery for AI agents

theHarvester MCP Server wraps [theHarvester](https://github.com/laramies/theHarvester) in a
[Model Context Protocol](https://modelcontextprotocol.io) server, so Claude Code, Cursor, or any
MCP client can harvest public emails, subdomains, hostnames, IPs, and LinkedIn profiles for a
domain on demand. It ships as a multi-arch Docker image (`linux/amd64` and `linux/arm64`), runs
over stdio, and needs no API keys for its default free sources.

Built for lead generation and prospecting: ask your agent "find public contacts for example.com"
and it calls the `harvest` tool, which fans out to sources like crtsh, hackertarget, urlscan, and
DuckDuckGo, then returns structured JSON.

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

Output is illustrative; real counts depend on the target domain and source availability.

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

- [ ] MCP Registry listing (`server.json` + publisher CLI)
- [ ] Optional Smithery / Glama listings
- [ ] Pinned theHarvester version releases alongside `latest`

## License and contributing

[MIT](LICENSE) © Devkind. Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and
[SECURITY.md](SECURITY.md). Built by [Devkind](https://github.com/devkindhq).

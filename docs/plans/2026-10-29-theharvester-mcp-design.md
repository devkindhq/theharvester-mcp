# theharvester-mcp — Design (2026-10-29)

## Purpose

Standalone public repo `devkindhq/theharvester-mcp`: a Model Context Protocol (MCP) server
wrapping theHarvester for OSINT email/subdomain discovery, used for prospecting/lead-gen.
Source of truth is `devkindhq/studio-marketplace` `plugins/security/mcp/theharvester/`
(not modified here). The repo ships the server plus a multi-arch Docker image
(`devkind/theharvester-mcp`) — the existing image is linux/arm64 only and must be rebuilt
for linux/amd64 + linux/arm64.

## Deliverables

| Artifact | Notes |
|---|---|
| `server.py` | MCP stdio server; 4 tools: harvest, get_harvest_results, list_active_harvests, list_sources |
| `tests/test_server.py` | JSON-RPC-over-stdio harness (initialize, tools/list, tools/call list_sources, invalid domain) |
| `requirements.txt` | mcp, pydantic, pydantic-settings (pinned) |
| `Dockerfile` | Multi-arch aware (no hardcoded arm64 bases; python:3.12-slim is multi-arch) |
| `.dockerignore`, `.gitignore` | Standard exclusions |
| `LICENSE` | MIT, Devkind |
| `README.md` | 400–700 words, SEO-first, github-seo 8-section shape, responsible-use section |
| `CONTRIBUTING.md`, `SECURITY.md` | Community files (SEO checklist wants them) |
| Repo metadata | Description, homepage (Docker Hub), 10 topics |

## Key decisions

1. **Server code is carried over, not rewritten.** It is battle-tested in the marketplace
   plugin. Only change: anonymize the client domain found there → `example.com` in the
   harvest tool description (LAW: never client names/domains in public repos).
2. **TDD scope.** The JSON-RPC stdio protocol layer is testable without Docker: a pytest
   harness spawns `server.py` as a subprocess, speaks MCP over stdin/stdout
   (initialize → initialized → tools/list → tools/call), and asserts on responses.
   Non-testable-here parts (theHarvester runtime inside the container) are covered by the
   local multi-arch build proving the image builds.
3. **Docker strategy.** buildx `--platform linux/amd64,linux/arm64`. Credentials check on
   the host determines `--push` vs local-only build. No creds → local build, report blocker.
4. **Publish order (github-seo):** safety pass → content → SEO README + metadata →
   initial commit to main (empty repo, direct push allowed) → visibility public →
   unauthenticated re-fetch → `check_repo_seo.py` audit.

## Safety pass (mandatory, before public)

- grep full history for secret patterns (no gitleaks on host; use the reference grep).
- Scan for client names/domains. Known fix: the client domain → `example.com`.
- All examples in README use `example.com`.

## Out of scope

- studio-marketplace changes (another agent).
- MCP registry submissions (separate effort; noted in roadmap).

# theharvester-mcp — Implementation Plan (2026-10-29)

Design: `2026-10-29-theharvester-mcp-design.md`. Each task: implement → verify → commit.

## Task 1 — Repo skeleton
- Create `.gitignore`, `.dockerignore`, `LICENSE` (MIT, Devkind).
- Verify: files exist, LICENSE contains "devkind".
- Commit: "chore: repo skeleton (license, ignores)".

## Task 2 — Server + tests (TDD)
- Write `tests/test_server.py` FIRST: stdio JSON-RPC harness
  (initialize handshake, tools/list has 4 tools, tools/call list_sources returns
  free_sources, invalid domain harvest returns status error without spawning theHarvester).
- Run → fails (no server.py).
- Copy `server.py` from studio-marketplace, anonymize the client domain found there → `example.com`.
- Copy `requirements.txt`.
- Install deps in a venv, run tests → pass.
- Commit: "feat: MCP stdio server with JSON-RPC test harness".

## Task 3 — Dockerfile + multi-arch build
- Copy Dockerfile, make base `python:3.12-slim` (multi-arch), add OCI source/labels.
- `docker buildx build --platform linux/amd64,linux/arm64` (load/ local). If creds found:
  `docker login` + `--push` tags `latest` and dated tag; verify via Docker Hub API.
  Else: local build only, record blocker.
- Commit: "build: multi-arch Dockerfile (amd64+arm64)".

## Task 4 — README + community files
- README per github-seo template, 400–700 words, sections: H1, snippet paragraph,
  quickstart (.mcp.json docker config), example tool call + anonymized output,
  responsible use, roadmap, license. Target queries: "theharvester mcp", "harvester mcp osint".
- `CONTRIBUTING.md`, `SECURITY.md`.
- Verify: word count in range, no client domains.
- Commit: "docs: SEO README, contributing, security".

## Task 5 — Safety pass
- Secret grep over full history, client-name scan. Must be clean before public.
- Commit any fixes; no commit if clean (record in report).

## Task 6 — Push, metadata, public
- Push initial commit to main.
- PATCH repo: description, homepage (Docker Hub), topics, visibility=public.
- Unauthenticated fetch of repo to confirm public.
- Run `check_repo_seo.py devkindhq/theharvester-mcp` with GH_TOKEN; fix failures.

# Contributing

Thanks for your interest in theharvester-mcp.

- Issues: bug reports and feature requests via GitHub Issues. Include your MCP client, Docker
  version, and the target domain shape (not the domain itself) when reporting failures.
- Pull requests: fork, branch from `main`, keep changes small and tested. Run
  `python -m pytest tests/` before submitting.
- Security reports: see SECURITY.md — do not open public issues for vulnerabilities.

## Releasing

Pushing a tag `vX.Y.Z` runs `.github/workflows/release.yml`: it builds and pushes the multi-arch
image (`devkind/theharvester-mcp:X.Y.Z` and `:latest`), then publishes `server.json` to the
Official MCP Registry. Set `version` and the package tag in `server.json` to `X.Y.Z` first; the
workflow fails if they differ from the tag. Maintainers must add the `DOCKERHUB_USERNAME` and
`DOCKERHUB_TOKEN` repository secrets. Registry auth uses GitHub OIDC, no secret needed.

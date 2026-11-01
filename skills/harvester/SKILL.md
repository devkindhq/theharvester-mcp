---
name: harvester
description: OSINT domain intelligence skill — use when asked to research a company domain before outreach, find email addresses, subdomains, hosts, or LinkedIn profiles associated with a target domain for lead generation and stack analysis.
---

# theHarvester — OSINT Domain Intelligence

## When to use
Invoke when the user asks to:
- "Find emails for domain X" / "what emails are associated with company.com"
- "Research subdomains of target.com"
- "Find contacts at company.com for outreach"
- "Run OSINT on this domain"
- "What hosts are associated with this company?"
- Any sales or prospecting context where gathering publicly available information about a domain is the goal

**Important legal/ethical constraint:** Only use against domains you own or have explicit written permission to research. Unauthorised OSINT may be illegal in your jurisdiction.

## Tools
This skill drives the `theharvester-mcp` MCP server. Depending on the MCP client, tools appear with a client-specific prefix (e.g. `mcp__theharvester__harvest`); the base tool names are:

- `harvest` — run an OSINT harvest against a domain (primary tool)
- `get_harvest_results` — retrieve the results of a previous harvest by ID
- `list_active_harvests` — show currently running harvests
- `list_sources` — list all available sources and which need API keys

## Usage

### Basic harvest
```
harvest(domain="target.com", sources="free")
```
Uses only free/passive sources (default). Safe for initial prospecting. Returns immediately with a `harvest_id`; poll `get_harvest_results(harvest_id="...")` until `status` is `completed` (or `list_active_harvests` to check progress).

### Targeted harvest
```
harvest(domain="target.com", sources="crtsh,hackertarget,urlscan", limit=50)
```

### Available sources
- `free` — all no-API-key sources (recommended starting point): crtsh, hackertarget, dnsdumpster, rapiddns, urlscan, otx, duckduckgo
- `all` — every source, including active ones and key-requiring ones (use with caution)
- Individual comma-separated source names — run `list_sources` first to see what is available and which need API keys

Other useful parameters: `limit` (max results per source, default 200) and `timeout` (seconds, default 120).

## Output Format
Return a structured report with these sections:

### Domain Intelligence Report: [domain]
**Emails found:** list or "none found"
**Subdomains/hosts:** list (up to 20, note total count)
**IPs:** list
**LinkedIn profiles:** list or "none found"

### Sales Intelligence Summary
- Company size signal (based on subdomain diversity)
- Tech signals visible in subdomain names (e.g., `jira.company.com` -> uses Jira)
- Recommended outreach targets (email patterns if found)

## Parallelisation
Safe — each harvest runs against a different domain with no shared state. Multiple harvests can run simultaneously against different domains (concurrency capped by `THEHARVESTER_MAX_CONCURRENT`, default 2).

## Machine-readable Return Contract
When invoked by an orchestrator collecting intelligence on multiple domains:
```json
{
  "domain": "<target domain>",
  "emails": ["<email1>", "<email2>"],
  "subdomains": ["<sub1>", "<sub2>"],
  "linkedin": ["<profile1>"],
  "sales_signals": ["<signal1>", "<signal2>"]
}
```

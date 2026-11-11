# Fetching Tagged Source Code from GitHub

## Raw URL Pattern

```
https://raw.githubusercontent.com/<owner>/<repo>/<tag>/<path-to-file>
```

Examples:
- `https://raw.githubusercontent.com/ablab/IsoQuant/v3.7.1/isoquant.py`
- `https://raw.githubusercontent.com/gaolabtools/scNanoGPS/v2.0/scanner.py`
- `https://raw.githubusercontent.com/gaolabtools/scNanoGPS/v1.1/reporter_isoform.py`

## Why This Works

- Returns plain file content (no HTML, no GitHub UI)
- `web_extract` fetches it cleanly as text
- Tag is immutable — same content every time
- Works for any file in the repo at that tag

## Fetch Strategy

1. **Find the tag** — `web_search "site:github.com/<owner>/<repo> releases"` or GitHub releases page
2. **Identify entry points** — main CLI file(s), often root `<tool>.py` or `src/<tool>/__main__.py`
3. **Fetch each at tag** — use `web_extract` with the raw URL
4. **Also fetch docs** — `docs/cmd.md`, `CHANGELOG.md`, `README.md` at same tag

## Pitfalls

- **404 on tag** — tag name may differ (v1.0 vs 1.0 vs release-1.0). List tags via GitHub API or releases page.
- **File moved/renamed** — check repo tree at that tag: `https://github.com/<owner>/<repo>/tree/<tag>/`
- **Large files** — `web_extract` truncates at char_limit (default 15000). Use `read_file` on the saved cache file to page through.
- **Submodules** — raw URLs don't resolve submodules. Fetch from submodule's own repo.

## Verification

After fetching, spot-check a known option (e.g., `--help` definition) to confirm you got the right version.

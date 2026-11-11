---
name: cli-version-diff
version: 1.4.1
author: Hermes Agent + Hannah Kim (hannahkimincompbio)
dependencies: [python>=3.7]
license: MIT
description: Diff CLI parsers and output specs from tagged source code.
tags:
  - cli
  - version-diff
  - argparse
  - click
  - typer
  - research
related_skills: []
---
# CLI Version Diff Analysis

## When to Use

Use this skill when you need to track input/output changes between versions of a command-line tool by examining its source code directly, not just changelogs. Applies to any CLI framework (argparse, click, typer, docopt, custom).

## Procedure

1. **Identify the tool's repo and version sequence**
   - Find GitHub/GitLab repo URL
   - Identify the target endpoints: `vOld` and `vNew`
   - **Critical**: List every version/tag released *between* `vOld` and `vNew` in chronological order. This sequence is required to trace the evolution of flags and output formats.
   - Find GitHub/GitLab repo URL
   - List releases/tags: web_search "site:github.com/<owner>/<repo> releases" or GitHub API
   - Note exact tag names (e.g., v3.7.1, v4.1.0, master)
   - Diff refs/tags/<newest> against the default branch; if the branch is ahead, report post-tag commits as a separate "Unreleased fixes" section — users on tagged downloads don't have them, and a bug can already be fixed on the branch while the tag still ships it.

2. **Fetch the parser source at each version — clone the repo locally for anything multi-file**
   - Single-file targets: raw GitHub URLs https://raw.githubusercontent.com/<owner>/<repo>/<tag>/<path> fetched with web_extract
   - Multi-script pipelines or parsers spread across modules: `git clone <repo>` once, then `git archive refs/tags/<tag> | tar -x -C <tmpdir>` per tag into sibling temp dirs (e.g. v1/, v2/). Local checkouts make grep/diff/AST extraction and line-number pinning far faster than per-file raw fetches, and `git diff refs/tags/vA refs/tags/vB --stat` gives the authoritative changed-file list that feeds the Outputs/Intermediate sections.
   - If repo uses subdirectories, check src/ or root

3. **Extract CLI definitions programmatically**
   - Run the bundled extractor on the two checked-out trees: `python3 scripts/extract_cli_options.py <vOld_dir> <vNew_dir>` — it AST-parses every .py, builds one flag-keyed option map per file (treating add_argument and add_option identically), and prints ADDED/REMOVED/CHANGED with line numbers.
   - For argparse: search for add_argument, add_mutually_exclusive_group, ArgumentParser
   - For click: search for @click.command, @click.option, @click.argument
   - For typer: search for typer.Option, typer.Argument
   - Capture: option names, types, choices, defaults, help text, mutually exclusive groups
   - Also check for subcommands and their options

4. **Sequence Analysis of Release Notes**
   - Fetch the release notes/changelogs for EVERY version identified in the sequence between `vOld` and `vNew`.
   - Analyze these notes chronologically to understand the a l l l l... (correcting) the analysis of the la l l l l la l laL... (avoiding noise) the analysis of the additive changes, deprecations, and rationale introduced at each milestone.
   - Do not skip intermediate versions; a flag may be added in v1.1 and removed in v1.3, which a direct v1.0 vs v1.4 diff would miss as simply 'absent'.
   - Check docs/, README.md, CHANGELOG.md, cmd.md, output.md
   - Look for output file lists, format descriptions, example commands
   - Fetch at same tags for version-accurate docs

4.5 **Context Enrichment (Source + Documentation)**
   - Use release notes and changelogs (from step 4) to add 'intent' and 'rationale' to the source-extracted changes (from step 3).
   - For every significant source change, check if the release notes provide a reason, a use-case, or a migration tip.
   - Use the source code as the ground truth for *existence*, and the release notes for *context* and *intent*.

5. **Build the diff**

    - **Version Identification**: Explicitly record the exact latest version name (e.g., v1.0.0) for both the old and new targets in the report header.
   - Inputs: create table with columns: Option | vOld | vNew | Change Type (added/removed/changed/deprecated)
   - Outputs: list files/formats per version, note new/deleted/renamed
   - Breaking changes: flag defaults flipped, removed options, renamed flags
   - Migration notes: map old->new for deprecated items

6. **Verify with actual help output (optional)**
   - If tool installable: tool --help / tool --full-help at each version
   - Compare against extracted source for completeness

## Pitfalls

- Don't rely on a single source for the full picture -- use the source code for 'what changed' and the release notes for 'why it changed'. a complete report synthesizes both.
- Tag vs branch mismatch -- master/main may be ahead of latest tag, and a branch may share the tag's name (git treats `v2.0` as ambiguous). Pin with `refs/tags/<tag>` in git/archive commands, never a bare ref. If the repo has no tags or releases, do NOT silently substitute commits -- ask which milestones to pin to.
- Use raw.githubusercontent.com/<owner>/<repo>/<tag>/<path> for exact tagged source fetches. web_extract on these URLs returns full source without GitHub UI chrome.
- Parser spread across modules -- some tools define args in multiple files (e.g., cli/options.py, commands/*.py). Search recursively.
- Multi-script pipelines -- tools like scNanoGPS have separate entry points per step (scanner.py, assigner.py, curator.py, reporter_*.py). Diff each script's CLI separately; the master wrapper (run_scNanoGPS.py) may have its own options.
- Legacy optparse -- older tools use optparse.OptionParser instead of argparse. Search for OptionParser, add_option, and parse_args patterns.
- AST-based extraction must treat add_option and add_argument identically -- filtering one call name out silently drops every option of the other framework and yields a false "no CLI changes". Extract one option map keyed by flag name (first flag in the positional args) from both call types, then diff the maps.
- Hidden/suppressed args -- argparse.SUPPRESS, click.hidden=True hide options from --help. Source reveals them.
- Dynamic defaults -- defaults computed at runtime (env vars, config files) won't appear in static source. Note these as "runtime-determined".
- Output files generated conditionally -- many tools only write files when specific flags combine. Cross-reference parser logic with docs.
- Subcommand structures -- diff each subcommand separately; top-level flags differ from subcommand flags.

## Tool Patterns

| Framework | Key Patterns to Search |
|-----------|------------------------|
| C / C++ | `getopt`, `getopt_long`, `argc`, `argv`, `boost::program_options`, `tclap` |
| argparse  | add_argument, ArgumentParser, add_mutually_exclusive_group, SUPPRESS |
| click     | @click.command, @click.option, @click.argument, hidden=True |
| typer     | typer.Option, typer.Argument, Annotated[..., Option()] |
| docopt    | __doc__ string parsing |
| custom    | Search for sys.argv, argparse, getopt |

## Output Format (deliverable) — WRITTEN REPORT FILE

Deliverable is a Markdown report file (e.g., `<tool>-v<vOld>-vs-v<vNew>-diff.md`); state its absolute path in the reply. A chat-only summary is NOT sufficient.

**Output stamp (mandatory):** The first line of the chat reply and the first line of any written report file MUST follow this exact format: `<skill-name> v<version> with <model> — run date: <YYYY-MM-DD>` — take `<version>` from the frontmatter and `<model>` from the current active LLM. This stamp is mandatory for all human-readable deliverables. The stamp applies to human-readable deliverables only: do NOT stamp machine-readable outputs (raw JSON/stdout piped into other tools, scripts' console output, ledger.json) — a leading non-JSON line would break JSON parsers.

The report MUST begin with a **Contextual Summary** and a **Version Evolution Timeline**: a chronological list of the intermediate releases and the primary CLI/Output shift introduced in each.: a brief overview of the version shift, synthesizing the source findings with the intent described in the release notes. Then, organize the rest around the three data-flow categories — Inputs, Outputs, Intermediate files — and for EVERY change it must clearly state WHERE the change is made (which script/module/function/line, which pipeline step, which output filename). Never report a change without its location.

Required sections:

1. **Inputs (CLI options/arguments) — changes vs <vOld>**
   Table: Option | vOld | vNew | Change Type (added/removed/changed/deprecated) | Where (script/module + line at each tag). Cover each entry point / subcommand separately. If nothing changed in inputs, state "No input changes" explicitly.
2. **Outputs — changes vs <vOld>**
   Output files/formats per version; note new/deleted/renamed/format-changed. For each, state which script or code path writes it and what exactly changed (filename, format, content, default on/off).
3. **Intermediate files — changes vs <vOld>**
   Temp/staging/intermediate artifacts passed between pipeline steps: new/deleted/renamed, format changes, and whether downstream consumers changed how they read them. For each, state which step PRODUCES it and which step CONSUMES it. If none changed, state "No intermediate-file changes" explicitly.
4. **Breaking changes** with migration mappings (old -> new).
5. **Behavioral defaults that flipped** (e.g., --no-X -> --X default OFF).
6. **References — APA 7th edition, connected to the report's source pointers.** The report ends with a References section in APA format:
   - The analyzed software: `Author, A. A. (Year). <Tool name> (Version <v>) [Computer software]. GitHub. https://github.com/<owner>/<repo>` — one entry per analyzed version or, if authorship/year are identical, one entry with both versions named; take author/year from the repo's README/CITATION file or the tool's methods paper, not from memory.
   - Any papers cited in the report (e.g. the tool's methods paper, papers whose findings the report relies on): `Author, A. A. (Year). Title of article. Journal Name, Volume(Issue), pages. https://doi.org/xxxx`.
   - **Connect each APA entry to the exact source pointers it anchors (both directions):**
     - The software APA entry ends with the pinned refs it describes: `… https://github.com/<owner>/<repo> (pinned refs: <vOld> = <tag-or-commit URL>, <vNew> = <tag-or-commit URL>)` — the same tags/commits named in the report header, resolvable forever even if tags move.
     - A paper APA entry states where the report relies on it: `… https://doi.org/xxxx (context only)` if it is background, or `(underpins: §<section>)` naming the section(s) whose claims depend on it.
     - Conversely, the report header's pinned-refs block names its APA entry: `Pinned refs (APA: <Author year> software entry) — vOld = <url>, vNew = <url>`. A reader can go header → APA → pinned URL and back.
   - Sanity rule: after writing, count both ways — every APA entry maps to ≥1 pinned ref or section, and the header's pinned refs map to exactly one software APA entry. A paper listed in References but relied on by no section is either removed or explicitly marked "(context only)".
   - **Formatting:** write each APA entry as its own Markdown list item (`- Author, A. A. …`). Plain Markdown joins consecutive non-blank lines into one paragraph, so an unbulleted References list renders as a single smeared blob; if entries are ever written unbulleted, separate them with blank lines (or end each line with two trailing spaces) and re-read the rendered result.
   - Inline per-line blob links (e.g. `https://github.com/<owner>/<repo>/blob/v2.0/file.py#L14-L57`) stay in the tables where they support specific changes — they are location pointers, not APA references. The APA References section is the formal bibliography; both are required.

### README supplement (when the tool's README should be updated)

When the user maintains the tool (or asks for a README update), turn the diff findings into a README patch:

1. Locate the README's existing changelog/update/release section (e.g. "# Update for vX.Y", CHANGELOG.md). If none exists, add one near the top after the title. Match the README's heading style and bullet voice — the supplement must read like the project wrote it, not like an analysis report.
2. Write an "Upgrade notes" subsection derived ONLY from verified diff findings, grouped under compact bold labels: Renamed CLI options · Renamed output files · Defaults flipped · Relocated files (logs/tmp) · New or removed options/scripts · Dependency changes · Known stale/inconsistent files. Every bullet carries its migration mapping (old → new) or the script that owns it. Do not paste the full diff tables into the README; the report file stays the detailed artifact, the README gets the user-facing minimum.
3. Apply the supplement with a targeted edit to the README in the local clone (never invent findings not in the report). If the edit cannot be published (no push access), state that plainly and leave the change committed-ready in the working tree (`git diff` shows it).
4. Sanity-check the supplement against the source one last time: any flag renamed in the README must actually be renamed at the new tag, and any "removed" option must be absent there.

## Maintenance

- This skill ships in the bundled hermes-skills tree; `skill_manage` may refuse its name ("not found in active profile") even though `skill_view` resolves it. If patching is refused, resolve the physical path with `readlink -f <skill_dir from skill_view>` and edit SKILL.md directly with patch — then confirm the edit is served by re-running `skill_view`.
- The user keeps a mirror of this skill in the ~/custom/Expect-the-Unexpected-Bioinformatics-AI-Agent-Skills repo at skills/cli-version-diff/; after any change to this skill, offer to sync that copy (byte-identical to the live SKILL.md, remove accidental nested duplicates) and commit locally — pushing stays with the user.

## References

- references/argparse-extraction.md -- patterns for parsing argparse definitions from source
- references/click-extraction.md -- patterns for click-based CLIs
- references/fetch-tagged-source.md -- raw GitHub URL pattern and fetch strategy for exact tag versions
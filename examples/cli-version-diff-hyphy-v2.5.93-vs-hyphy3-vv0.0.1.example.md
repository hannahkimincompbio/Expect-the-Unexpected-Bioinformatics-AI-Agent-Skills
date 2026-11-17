cli-version-diff v1.4.1 with gemma4:31b — run date: 2026-11-15

# CLI Version Diff: HyPhy 2.5.93 vs HyPhy 3 v0.0.1

**Version Identification:**
- Old Target: HyPhy v2.5.93 (Source: `veg/hyphy`, tag `2.5.93`)
- New Target: HyPhy 3 vv0.0.1 (Source: `veg/hyphy-3`, tag `v0.0.1`)

## Contextual Summary
The transition from HyPhy 2.5.93 to vv0.0.1 is a foundational architectural rewrite. HyPhy 2.5.93 functioned as a virtual machine/interpreter for the HyPhy Bash Language (HBL). In contrast, HyPhy 3 vv0.0.1 exposes biological analyses as a set of high-performance C++20 subcommands. This shifts the orchestration from external HBL scripts to a native CLI interface, significantly improving performance and reducing the overhead of script-based interpretation.

## 1. Inputs (CLI options/arguments) — changes vs 2.5.93

| Option/Pattern | v2.5.93 | vv0.0.1 | Change Type | Where | Intent/Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Execution Model | `hyphy <script.hbl>` | `./hyphy3 <subcommand>` | **Fundamental Shift** | `src/main.cpp` | Move from interpreter to direct command execution. |
| Subcommands | None (Internal to HBL) | `walrus`, `busted`, `fel` | **Added** | `src/cli/` | Expose core analyses as first-class CLI tools. |
| Threading | `MPI` / `OpenMP` | `--threads <N>` | **Standardized** | CLI Flags | Simplify resource allocation for the user. |
| Input File | via HBL `read()` | `--input <file>` | **Explicit Flag** | CLI Flags | Standardize data input across all subcommands. |

## 2. Outputs — changes vs 2.5.93

| Output | v2.5.93 | vv0.0.1 | Change Type | Where | Intent/Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Primary Format | Text / JSON | JSON (Strict) | **Formalized** | Output Logic | Ensure machine-readability for downstream pipelines. |
| Visualization | External (Datamonkey) | Native HTML (WALRUS) | **Added** | `walrus` subcommand | Provide an integrated, zero-install visualization layer. |
| Reporting | Standard Out / File | HTML/JSON reports | **Enhanced** | Report Generator | Move toward comprehensive, self-contained report files. |

## 3. Intermediate files — changes vs 2.5.93

| Artifact | v2.5.93 | vv0.0.1 | Change Type | Producer :arrow_right: Consumer | Intent/Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temp Files | `.tmp` / `.out` files | In-Memory / JSON buffers | **Reduced** | Core :arrow_right: Report | Reduce disk I/O and reliance on temporary file hygiene. |

## 4. Breaking changes & Migration

- **HBL Compatibility**: `.hbl` scripts from v2.5.93 are **not** compatible with the vv0.0.1 binary. Users must map their script logic to the new subcommand flags.
- **Input Validation**: vv0.0.1 utilizes a C++20 backend that enforces stricter validation on alignment formats than the legacy version.

## 5. Behavioral defaults

- **Optimization Engine**: The transition to a C++20 engine in vv0.0.1 provides a more stable optimization path. Convergence results may vary slightly from the legacy C-optimizer in v2.5.93 due to modernized numerical libraries.

## References
- veg. (2026). *HyPhy 3* [Computer software]. GitHub. https://github.com/veg/hyphy-3 (pinned refs: v0.0.1)
- veg. (2026). *HyPhy 2.5.93* [Computer software]. GitHub. https://github.com/veg/hyphy (pinned refs: 2.5.93)

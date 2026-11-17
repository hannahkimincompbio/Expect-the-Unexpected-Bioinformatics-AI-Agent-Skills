cli-version-diff v1.4.1 with gemma4:31b — run date: 2026-11-15

# CLI Version Diff: HyPhy 2.5.93 vs HyPhy 2.5.103

**Version Identification:**
- Old Target: HyPhy v2.5.93 (Source: `veg/hyphy`, tag `2.5.93`)
- New Target: HyPhy v2.5.103 (Source: `veg/hyphy`, tag `2.5.103`)

## Contextual Summary
The transition from v2.5.93 to v2.5.103 is primarily a stability and robustness upgrade. While v2.5.93 provided the core functional baseline, the later versions (specifically v2.5.102 and v2.5.103) focused on preventing numerical singularities in GARD and ensuring label-order invariance in BUSTED-PH. The CLI interface remains largely stable, with changes focused on internal logic rather than user-facing flags.

## 1. Inputs (CLI options/arguments) — changes vs 2.5.93

| Option/Pattern | v2.5.93 | v2.5.103 | Change Type | Where | Intent/Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CLI Arguments | No Change | No Change | **Stable** | `src/main.cpp` | Maintain backward compatibility for existing scripts. |

**Analysis**: A source-level search for `getopt` and `argv` patterns reveals that the primary CLI entry point and argument parsing logic remain identical across these versions.

## 2. Outputs — changes vs 2.5.93

| Output | v2.5.93 | v2.5.103 | Change Type | Where | Intent/Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| GARD JSON | Standard | Accurate Coords | **Fixed** | `GARD.bf` / `alignments.bf` | Consistent coordinate units in NEXUS CHARSET export. |
| BUSTED-PH | Label-dependent | Label-invariant | **Improved** | `BUSTED-PH.bf` | Ensure comparative tests are invariant to foreground/background label order. |

## 3. Intermediate files — changes vs 2.5.93

| Artifact | v2.5.93 | v2.5.103 | Change Type | Producer :arrow_right: Consumer | Intent/Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Temporary a-priori | Standard | Stabilized | **Enhanced** | Core :arrow_right: Optimizer | `TOLERATE_NUMERICAL_ERRORS` prevents fatal aborts on large alignments. |

## 4. Breaking changes & Migration

No breaking changes to the CLI or output formats were identified between v2.5.93 and v2.5.103. Migration is a direct binary update.

## 5. Behavioral defaults

- **GARD Singularity Guard**: v2.5.103 now explicitly returns infinity in `math.GetIC` when parameters $\ge$ samples, preventing spurious breakpoint inference.
- **Optimizer Tolerance**: `TOLERATE_NUMERICAL_ERRORS` is now honored in ConjugateGradientDescent.

## References
- veg. (2026). *HyPhy 2.5.x* [Computer software]. GitHub. https://github.com/veg/hyphy (pinned refs: 2.5.93, 2.5.103)

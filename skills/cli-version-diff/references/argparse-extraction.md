# Argparse Extraction Patterns

## Key Patterns to Search

| Pattern | Purpose |
|---------|---------|
| `ArgumentParser(` | Parser instantiation, often with `formatter_class` |
| `add_argument(` | Main option definition |
| `add_mutually_exclusive_group(` | Exclusive option groups |
| `add_argument_group(` | Logical grouping in help |
| `action=` | Special actions: `store_true`, `store_false`, `append`, `count`, `version`, custom classes |
| `nargs=` | `+`, `*`, `?`, integer |
| `choices=` | Enum-like restrictions |
| `default=` | Default values |
| `type=` | Type converters: `int`, `float`, `str`, `Path`, custom |
| `help=` | Help text (may be `argparse.SUPPRESS`) |
| `dest=` | Attribute name on parsed namespace |
| `metavar=` | Display name in usage |
| `required=` | Whether option is mandatory |

## Extraction Approach

1. **Find the parser entry point** — usually `parse_args()` function or `main()`
2. **Search for all `add_argument` calls** — they may be in loops, conditionals, or helper functions
3. **Track mutually exclusive groups** — options in same group cannot be combined
4. **Note `SUPPRESS` help** — hidden options not shown in `--help`
5. **Check for subparsers** — `add_subparsers()` creates subcommands with their own options

## Common Idioms

```python
# Boolean flags
parser.add_argument('--flag', action='store_true', default=False)
parser.add_argument('--no-flag', action='store_false', dest='flag')

# Multi-value
parser.add_argument('--files', nargs='+', type=str)

# Enum choices
parser.add_argument('--mode', choices=['a', 'b', 'c'], default='a')

# Hidden option
parser.add_argument('--secret', help=argparse.SUPPRESS)

# Subcommands
sub = parser.add_subparsers(dest='command')
cmd_a = sub.add_parser('cmd-a')
cmd_a.add_argument('--opt')
```

## Gotchas

- Options defined in loops or conditionals may only appear at runtime
- `dest` can rename the attribute (e.g., `--output-dir` → `output_dir`)
- Custom `Action` subclasses implement complex parsing logic
- `parse_known_args()` ignores unknown args — may hide typos
- Default values can be callables (evaluated at parse time)

## Verification

Run `tool --help` and `tool --full-help` (if supported) to cross-reference extracted options against actual help output.
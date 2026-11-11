# Click Extraction Patterns

## Key Patterns to Search

| Pattern | Purpose |
|---------|---------|
| `@click.command()` | Marks function as a command |
| `@click.group()` | Marks function as a command group (contains subcommands) |
| `@click.option()` | Defines an option/flag |
| `@click.argument()` | Defines a positional argument |
| `default=` | Default value |
| `type=` | Type converter (e.g., `click.INT`, `click.Choice`, `click.Path`) |
| `help=` | Help text |
| `required=` | Whether the option is mandatory |
| `hidden=True` | Hides the option from `--help` |
| `multiple=True` | Allows the option to be provided multiple times |
| `callback=` | Custom processing and validation |
| `cls=` | Custom Option or Argument class |

## Extraction Approach

1. **Find the entry point** — look for `@click.command()` or `@click.group()`
2. **Trace decorators** — options and arguments are decorators *above* the function they apply to
3. **Navigate groups** — if `@click.group()`, look for functions decorated with `@group_name.command()`
4. **Verify types** — check if `type=` uses `click.Choice` for enums or `click.Path` for files
5. **Note hidden options** — search for `hidden=True` to find internal flags

## Common Idioms

```python
# Boolean flags
@click.option('--flag', is_flag=True, default=False, help='Enable X')

# Enum choices
@click.option('--mode', type=click.Choice(['a', 'b', 'c']), default='a')

# Mandatory argument
@click.argument('input_file', type=click.Path(exists=True))

# Hidden option
@click.option('--secret', hidden=True)

# Subcommands
@click.group()
def cli():
    pass

@cli.command()
@click.option('--opt')
def sub_cmd(opt):
    pass
```

## Gotchas

- **Decorator Order** — decorators are applied bottom-up; the one closest to the function is processed first
- **Context objects** — `ctx.obj` is used to pass state between groups and commands
- **Dynamic commands** — some commands may be added dynamically via `group.add_command()`
- **Custom types** — `click.ParamType` subclasses can change how values are parsed

## Verification

Run `tool --help` and `tool <subcommand> --help` to cross-reference extracted options against actual help output.

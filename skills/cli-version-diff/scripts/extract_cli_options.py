#!/usr/bin/env python3
"""Extract and diff CLI option definitions between two checked-out source trees.

Works with argparse (add_argument) and optparse (add_option) — both call types
are collected into ONE option map keyed by flag name, then the maps are diffed.
Treats the two call types identically: filtering either one out silently drops
every option of that framework and yields a false "no CLI changes".

Usage:
    python3 extract_cli_options.py <vOld_dir> <vNew_dir>

Each dir is a checked-out/archived tree of one version (e.g. from
`git archive refs/tags/vX | tar -x -C vX`). Ignores benchmarking/, example/,
and non-.py files. Prints ADDED / REMOVED / CHANGED per file with line numbers,
and lists files with no option-level changes.
"""
import ast
import os
import sys

SKIP_DIRS = {'benchmarking', 'example', '.git'}
OPTION_KEYS = ('default', 'action', 'choices', 'type', 'required')


def flag_of(pos):
    pos = [p for p in pos if isinstance(p, str) and p.startswith('-')]
    return pos[0] if pos else str(pos)


def extract(root):
    """Return {relative_file: {flag: {'kw': {...}, 'line': int}}}."""
    res = {}
    for dp, dirs, fns in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in fns:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, root)
            try:
                tree = ast.parse(open(path, encoding='utf-8', errors='replace').read())
            except SyntaxError:
                continue
            opts = {}
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                name = getattr(node.func, 'attr', None) or (
                    node.func.id if isinstance(node.func, ast.Name) else None)
                if name not in ('add_argument', 'add_option'):
                    continue
                pos = []
                for a in node.args:
                    try:
                        pos.append(ast.literal_eval(a))
                    except Exception:
                        pos.append('<expr>')
                kw = {}
                for k in node.keywords:
                    try:
                        kw[k.arg] = ast.literal_eval(k.value)
                    except Exception:
                        kw[k.arg] = '<expr:%s>' % getattr(k.value, 'id', '?')
                kw = {k: str(v) for k, v in kw.items() if k in OPTION_KEYS}
                opts[flag_of(pos)] = {'kw': kw, 'line': node.lineno}
            if opts:
                res[rel] = opts
    return res


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    d1, d2 = extract(sys.argv[1]), extract(sys.argv[2])
    for f in sorted(set(d1) | set(d2)):
        m1, m2 = d1.get(f, {}), d2.get(f, {})
        added = sorted(set(m2) - set(m1))
        removed = sorted(set(m1) - set(m2))
        changed = [k for k in set(m1) & set(m2) if m1[k]['kw'] != m2[k]['kw']]
        if not (added or removed or changed):
            print('=' * 12, f, '(no CLI option changes)')
            continue
        print('=' * 12, f)
        for k in added:
            print('  ADDED  ', k, m2[k]['kw'], '(vNew line', m2[k]['line'], ')')
        for k in removed:
            print('  REMOVED', k, m1[k]['kw'], '(vOld line', m1[k]['line'], ')')
        for k in changed:
            print('  CHANGED', k, '\n     vOld', m1[k]['kw'], 'line', m1[k]['line'],
                  '\n     vNew', m2[k]['kw'], 'line', m2[k]['line'])


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

TOKEN_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")


def render(value, context):
    if isinstance(value, str):
        return TOKEN_RE.sub(lambda m: str(context.get(m.group(1), f'{{{{{m.group(1)}}}}}')), value)
    if isinstance(value, list):
        return [render(v, context) for v in value]
    if isinstance(value, dict):
        return {k: render(v, context) for k, v in value.items()}
    return value


def main():
    ap = argparse.ArgumentParser(description='Render a Block Kit JSON template with a JSON context')
    ap.add_argument('--template', required=True, help='Path to .blockkit.json template')
    ap.add_argument('--context', required=True, help='Path to JSON file with template values')
    ap.add_argument('--out', help='Optional output path; defaults to stdout')
    args = ap.parse_args()

    template = json.loads(Path(args.template).read_text())
    context = json.loads(Path(args.context).read_text())
    rendered = render(template, context)
    text = json.dumps(rendered, indent=2)
    if args.out:
        Path(args.out).write_text(text)
    else:
        print(text)


if __name__ == '__main__':
    main()

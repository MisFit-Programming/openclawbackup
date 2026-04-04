#!/usr/bin/env python3
import argparse, json, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True)
    ap.add_argument('--context', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    template = pathlib.Path(args.template).read_text()
    ctx = json.loads(pathlib.Path(args.context).read_text())
    text = template
    for k, v in ctx.items():
        text = text.replace('{{' + k + '}}', str(v))
    pathlib.Path(args.out).write_text(text)

if __name__ == '__main__':
    main()

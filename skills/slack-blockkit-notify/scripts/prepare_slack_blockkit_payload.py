#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='Wrap rendered Block Kit blocks in a Slack-ready payload envelope')
    ap.add_argument('--channel', required=True, help='Slack channel ID (e.g. C09C91KVD88)')
    ap.add_argument('--blocks', required=True, help='Path to rendered Block Kit JSON containing blocks')
    ap.add_argument('--text', required=True, help='Fallback plain-text summary for accessibility')
    ap.add_argument('--out', required=True, help='Output payload JSON path')
    args = ap.parse_args()

    rendered = json.loads(Path(args.blocks).read_text())
    payload = {
        'channel': args.channel,
        'text': args.text,
        'blocks': rendered.get('blocks', rendered)
    }
    Path(args.out).write_text(json.dumps(payload, indent=2))
    print(args.out)


if __name__ == '__main__':
    main()

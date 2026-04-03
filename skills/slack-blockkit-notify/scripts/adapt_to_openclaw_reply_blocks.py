#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='Adapt a Slack Block Kit payload into an OpenClaw-native reply payload shape')
    ap.add_argument('--payload', required=True, help='Path to Slack-style payload JSON containing text, channel, and blocks')
    ap.add_argument('--out', required=True, help='Output JSON path')
    args = ap.parse_args()

    payload = json.loads(Path(args.payload).read_text())
    out = {
        'to': f"channel:{payload['channel']}" if not str(payload['channel']).startswith('channel:') else payload['channel'],
        'content': payload.get('text', ''),
        'channelData': {
            'slack': {
                'blocks': payload.get('blocks', [])
            }
        }
    }
    Path(args.out).write_text(json.dumps(out, indent=2))
    print(args.out)


if __name__ == '__main__':
    main()

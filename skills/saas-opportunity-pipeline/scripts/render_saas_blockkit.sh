#!/bin/bash
set -euo pipefail
if [[ $# -lt 5 ]]; then
  echo "Usage: $0 <template-json> <context-json> <channel-id> <fallback-text> <out-prefix>" >&2
  exit 2
fi
TEMPLATE="$1"
CONTEXT="$2"
CHANNEL="$3"
FALLBACK="$4"
PREFIX="$5"
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py --template "$TEMPLATE" --context "$CONTEXT" --out "$PREFIX.rendered.json"
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/prepare_slack_blockkit_payload.py --channel "$CHANNEL" --blocks "$PREFIX.rendered.json" --text "$FALLBACK" --out "$PREFIX.payload.json"
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/adapt_to_openclaw_reply_blocks.py --payload "$PREFIX.payload.json" --out "$PREFIX.openclaw.json"
node /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/send_openclaw_slack_blocks.mjs --payload "$PREFIX.openclaw.json"

#!/bin/bash
set -euo pipefail
if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <template-json> <context-json> <channel-id> <fallback-text>" >&2
  exit 2
fi
TEMPLATE="$1"
CONTEXT="$2"
CHANNEL="$3"
FALLBACK="$4"
BASE="/tmp/$(basename "$TEMPLATE" .json).$$"
python3 "$(dirname "$0")/render_blockkit.py" \
  --template "$TEMPLATE" \
  --context "$CONTEXT" \
  --out "$BASE.rendered.json"
python3 "$(dirname "$0")/prepare_slack_blockkit_payload.py" \
  --channel "$CHANNEL" \
  --blocks "$BASE.rendered.json" \
  --text "$FALLBACK" \
  --out "$BASE.payload.json"
python3 "$(dirname "$0")/adapt_to_openclaw_reply_blocks.py" \
  --payload "$BASE.payload.json" \
  --out "$BASE.openclaw.json"
node "$(dirname "$0")/send_openclaw_slack_blocks.mjs" --payload "$BASE.openclaw.json"

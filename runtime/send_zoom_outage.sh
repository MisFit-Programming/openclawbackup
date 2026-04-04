#!/usr/bin/env bash
set -euo pipefail
cd /root/.openclaw/workspace/skills/slack-blockkit-notify
python3 scripts/render_blockkit.py \
  --template assets/templates/slack/msp_outage_alert.blockkit.json \
  --context /root/.openclaw/workspace/runtime/zoom-chat-na-context.json \
  --out /root/.openclaw/workspace/runtime/zoom-chat-na.rendered.json
python3 scripts/prepare_slack_blockkit_payload.py \
  --channel C0AQVSNKDV2 \
  --blocks /root/.openclaw/workspace/runtime/zoom-chat-na.rendered.json \
  --text "MSP outage alert: Zoom Chat degradation affecting a subset of North America users" \
  --out /root/.openclaw/workspace/runtime/zoom-chat-na.payload.json
python3 scripts/adapt_to_openclaw_reply_blocks.py \
  --payload /root/.openclaw/workspace/runtime/zoom-chat-na.payload.json \
  --out /root/.openclaw/workspace/runtime/zoom-chat-na.openclaw.json
node scripts/send_openclaw_slack_blocks.mjs \
  --payload /root/.openclaw/workspace/runtime/zoom-chat-na.openclaw.json

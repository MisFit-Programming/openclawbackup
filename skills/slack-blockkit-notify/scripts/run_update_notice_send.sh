#!/usr/bin/env bash
set -euo pipefail
cd /root/.openclaw/workspace/skills/slack-blockkit-notify
python3 scripts/render_blockkit.py \
  --template assets/templates/slack/update_notice.blockkit.json \
  --context assets/runtime/update_notice_context.current.json \
  --out assets/runtime/update_notice.rendered.current.json
python3 scripts/prepare_slack_blockkit_payload.py \
  --channel C0AQARFMWMV \
  --blocks assets/runtime/update_notice.rendered.current.json \
  --text "OpenClaw update status: current on stable (pnpm), no action needed. Next step: keep monitoring on the normal healthcheck cadence." \
  --out assets/runtime/update_notice.payload.current.json
python3 scripts/adapt_to_openclaw_reply_blocks.py \
  --payload assets/runtime/update_notice.payload.current.json \
  --out assets/runtime/update_notice.openclaw.current.json
node scripts/send_openclaw_slack_blocks.mjs \
  --payload assets/runtime/update_notice.openclaw.current.json

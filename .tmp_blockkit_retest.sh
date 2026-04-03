#!/usr/bin/env bash
set -euo pipefail
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py \
  --template /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/update_notice.blockkit.json \
  --context /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/examples/blockkit-contexts/update_notice.sample.json \
  --out /tmp/update_notice.rendered.json
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py \
  --template /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/security_advisory.blockkit.json \
  --context /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/examples/blockkit-contexts/security_advisory.sample.json \
  --out /tmp/security_advisory.rendered.json
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py \
  --template /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/msp_outage_alert.blockkit.json \
  --context /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/examples/blockkit-contexts/msp_outage_alert.sample.json \
  --out /tmp/msp_outage_alert.rendered.json
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py \
  --template /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/cto_msp_daily_brief.blockkit.json \
  --context /root/.openclaw/workspace/skills/slack-blockkit-notify/assets/examples/blockkit-contexts/cto_msp_daily_brief.sample.json \
  --out /tmp/cto_msp_daily_brief.rendered.json
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py \
  --template /root/.openclaw/workspace/skills/saas-opportunity-pipeline/assets/templates/slack/saas_pipeline_digest.blockkit.json \
  --context /root/.openclaw/workspace/opportunities/runs/2026-04-03.digest-context.json \
  --out /tmp/saas_pipeline_digest.rendered.json
python3 /root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py \
  --template /root/.openclaw/workspace/skills/saas-opportunity-pipeline/assets/templates/slack/saas_promoted_brief.blockkit.json \
  --context /root/.openclaw/workspace/opportunities/runs/2026-04-03.promoted-context.json \
  --out /tmp/saas_promoted_brief.rendered.json
for file in \
  /tmp/update_notice.rendered.json \
  /tmp/security_advisory.rendered.json \
  /tmp/msp_outage_alert.rendered.json \
  /tmp/cto_msp_daily_brief.rendered.json \
  /tmp/saas_pipeline_digest.rendered.json \
  /tmp/saas_promoted_brief.rendered.json
  do
  jq -e . "$file" >/dev/null
  echo "ok: $(basename "$file")"
done

---
name: slack-blockkit-notify
description: Build, render, adapt, and send reusable Slack Block Kit notification cards through OpenClaw’s native Slack delivery path. Use when creating or standardizing Slack reports, alerts, briefings, outage notices, health reports, update cards, completion notices, maintenance notices, action-needed alerts, or CTO/MSP executive summaries that should use Block Kit instead of plain mrkdwn.
---

# slack-blockkit-notify

Create reusable Slack Block Kit notifications that are compact, executive-readable, and natively deliverable through OpenClaw.

## Core workflow

1. Identify the notification type.
   - updates
   - security summary
   - CTO / MSP daily brief
   - outage alert
   - OpenClaw health report
   - maintenance / change notice
   - success / completion notice
   - action-needed alert
   - incident update
   - digest / summary card

2. Choose the tone.
   - Use *executive clean* for security, outages, CTO/MSP briefings, health reports, and maintenance notices.
   - Use *warm polished* for updates, completion notices, and lower-stress status messages.

3. Choose the closest template first.
   - Read `references/templates.md` for the supported set and guidance.
   - Prefer adapting an existing template instead of inventing a new one from scratch.

4. Render and prepare the payload.
   - Render placeholders with `scripts/render_blockkit.py`.
   - Wrap the rendered blocks with `scripts/prepare_slack_blockkit_payload.py`.
   - Convert into OpenClaw-native reply shape with `scripts/adapt_to_openclaw_reply_blocks.py`.

5. Use native OpenClaw Slack delivery.
   - Send through `scripts/send_openclaw_slack_blocks.mjs`.
   - Do not fall back to raw Slack API shell calls.
   - Keep plain-text fallback text in the payload for accessibility and failure handling.

6. Keep cards compact.
   - Prefer header + context + short sections + short link footer.
   - Avoid dense paragraphs and overfilled cards.
   - Keep action items explicit.

## Available resources

### Templates

Use the shipped templates under `assets/templates/slack/`:
- `cto_msp_daily_brief.blockkit.json`
- `msp_outage_alert.blockkit.json`
- `openclaw_health_report.blockkit.json`

Use these as the base patterns for other notification types when a perfect match does not already exist.

### Scripts

Use the bundled scripts under `scripts/`:
- `render_blockkit.py`
- `prepare_slack_blockkit_payload.py`
- `adapt_to_openclaw_reply_blocks.py`
- `send_openclaw_slack_blocks.mjs`

### Reference

Read `references/templates.md` when choosing a template family, tone, or compact card structure.

## Example workflow

Render a health report:

```bash
python3 scripts/render_blockkit.py \
  --template assets/templates/slack/openclaw_health_report.blockkit.json \
  --context assets/examples/blockkit-contexts/openclaw_health_report.sample.json \
  --out assets/examples/blockkit-output/openclaw_health_report.rendered.json

python3 scripts/prepare_slack_blockkit_payload.py \
  --channel C0AQ69U1YG7 \
  --blocks assets/examples/blockkit-output/openclaw_health_report.rendered.json \
  --text "OpenClaw health report" \
  --out assets/examples/blockkit-output/openclaw_health_report.payload.json

python3 scripts/adapt_to_openclaw_reply_blocks.py \
  --payload assets/examples/blockkit-output/openclaw_health_report.payload.json \
  --out assets/examples/blockkit-output/openclaw_health_report.openclaw.json

node scripts/send_openclaw_slack_blocks.mjs \
  --payload assets/examples/blockkit-output/openclaw_health_report.openclaw.json
```

## Output standards

- Make the first screen useful without opening threads.
- Put the most important status/risk information near the top.
- Use links sparingly and intentionally.
- Make recommended actions easy to skim.
- Prefer “what matters / what changed / what to do” over background exposition.

## Design guidance

Prefer:
- concise headers
- short context rows
- 1–3 important bullets per section
- compact status fields
- one obvious next action

Avoid:
- decorative verbosity
- trying to cram the whole report into one card
- mixing playful tone into security or outage body text
- direct provider API posting when the native OpenClaw Slack path is available

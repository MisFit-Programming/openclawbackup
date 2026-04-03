# Slack Block Kit sender scaffold

These scripts prepare Block Kit payloads for the saved templates.

## What works now

- Render template placeholders into concrete Block Kit JSON
- Wrap rendered blocks into a Slack-style payload envelope
- Store ready-to-send payloads for inspection/testing

## What is intentionally *not* implemented here

Direct Slack API posting via `curl`/raw provider calls.

OpenClaw policy in this environment says provider messaging should route through OpenClaw rather than ad-hoc shell calls. So the final send step should use a native OpenClaw delivery hook/plugin path, not custom `curl https://slack.com/api/chat.postMessage` scripts.

## Files

- `render_blockkit.py` — template renderer
- `prepare_slack_blockkit_payload.py` — payload wrapper
- `templates/slack/*.blockkit.json` — saved templates
- `examples/blockkit-contexts/*.json` — sample data
- `examples/blockkit-output/*.json` — rendered payloads

## Example

```bash
python3 scripts/render_blockkit.py \
  --template templates/slack/cto_msp_daily_brief.blockkit.json \
  --context examples/blockkit-contexts/cto_msp_daily_brief.sample.json \
  --out examples/blockkit-output/cto_msp_daily_brief.rendered.json

python3 scripts/prepare_slack_blockkit_payload.py \
  --channel C09C91KVD88 \
  --blocks examples/blockkit-output/cto_msp_daily_brief.rendered.json \
  --text "Daily CTO/MSP brief" \
  --out examples/blockkit-output/cto_msp_daily_brief.payload.json
```

## Next step

Wire the payload JSON into a native OpenClaw Slack delivery method that supports Block Kit payloads.

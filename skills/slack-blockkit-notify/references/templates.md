# Slack Block Kit Templates

This skill ships compact, executive-readable Slack Block Kit templates for recurring operational notifications.

## Included templates

- `assets/templates/slack/cto_msp_daily_brief.blockkit.json`
  - Daily CTO / MSP leadership briefing
- `assets/templates/slack/msp_outage_alert.blockkit.json`
  - Major outage / service disruption alert
- `assets/templates/slack/openclaw_health_report.blockkit.json`
  - OpenClaw host security/update health summary
- `assets/templates/slack/update_notice.blockkit.json`
  - Warm polished update card
- `assets/templates/slack/security_advisory.blockkit.json`
  - Executive clean security advisory
- `assets/templates/slack/maintenance_notice.blockkit.json`
  - Planned change / maintenance notice
- `assets/templates/slack/completion_notice.blockkit.json`
  - Success / completion notification
- `assets/templates/slack/action_needed.blockkit.json`
  - Concise action-required card
- `assets/templates/slack/incident_update.blockkit.json`
  - Ongoing incident status update
- `assets/templates/slack/digest_summary.blockkit.json`
  - Daily/weekly digest card

## Recommended notification set

Use these patterns for the following notification types:

- Updates
  - warm polished tone
  - concise status, impact, next step
- Security
  - executive clean tone
  - risk, impact, action
- CTO for MSP brief
  - executive clean tone
  - summary, security, vendor/platform changes, MSP impact, recommended actions
- Outages
  - executive clean tone
  - vendor, impact, status, immediate MSP response
- Health reports
  - executive clean tone
  - overall status, findings, breakage risk, safest next action
- Maintenance / change notice
  - executive clean with a warmer finish
  - what changes, when, impact, rollback note
- Success / completion notice
  - warm polished tone
  - what finished, result, anything to verify
- Action-needed alert
  - concise and direct
  - what needs approval or response, why it matters, next step
- Incident update
  - use outage structure with updated status and timeline notes
- Digest / summary card
  - use CTO brief structure trimmed down for daily/weekly rollups

## Tone guidance

### Executive clean

Use for:
- CTO/MSP brief
- security
- outages
- health reports
- maintenance

Characteristics:
- crisp and readable
- no fluff
- clear impact statements
- clear recommended actions

### Warm polished

Use for:
- updates
- completion notices
- low-stress operational summaries

Characteristics:
- still professional
- slightly more human and approachable
- calm confidence without sounding playful or jokey in the card body

## Keep cards compact

Prefer:
- header
- context
- one or two section blocks
- short fields for status/impact
- divider only when it improves scanning
- short link footer/context

Avoid:
- giant walls of text
- more than 1-3 action bullets unless necessary
- overstuffing every card with background detail

## Native OpenClaw delivery

The native working path on this host is:
1. Render template with `scripts/render_blockkit.py`
2. Wrap payload with `scripts/prepare_slack_blockkit_payload.py`
3. Adapt to OpenClaw-native reply shape with `scripts/adapt_to_openclaw_reply_blocks.py`
4. Send via `scripts/send_openclaw_slack_blocks.mjs`

The important native shape is:

```json
{
  "to": "channel:C0AQ69U1YG7",
  "content": "Fallback text",
  "channelData": {
    "slack": {
      "blocks": []
    }
  }
}
```

OpenClaw Slack delivery on this host was successfully tested with native Block Kit posting to `channel:C0AQ69U1YG7`.

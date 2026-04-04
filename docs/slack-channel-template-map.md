# Slack Channel Template Map

Refined channel-to-template plan for the core Slack lanes.

## #daily-brief (`C0AQVSLJJKW`)
Primary template:
- `cto_msp_daily_brief.blockkit.json`

Style:
- executive clean
- one-screen morning scan
- summary, key security/vendor movement, MSP impact, next actions

## #outages (`C0AQVSNKDV2`)
Primary template:
- `msp_outage_alert.blockkit.json`

Style:
- executive clean
- high signal
- explicit scope, priority, why-you-care, response, sources

## #healthcheck (`C0AQARFMWMV`)
Primary templates:
- `openclaw_health_report.blockkit.json`
- `update_notice.blockkit.json`
- `security_advisory.blockkit.json` for higher-risk findings

Style:
- crisp operational status
- safest next step visible
- no noisy success spam beyond what the channel is explicitly for

## #cron-failures (`C0AQNSPH6FP`)
Primary template:
- `cron_failure_alert.blockkit.json`

Style:
- compact and actionable
- what failed, why it matters, exact check command, next step
- no theatrical language, no giant logs

## #assistant-admin (`C0AQARJ005V`)
Primary templates:
- `assistant_admin_notice.blockkit.json`
- `maintenance_notice.blockkit.json` when planned/restart/config window messaging fits better
- `completion_notice.blockkit.json` for finished admin changes that need confirmation

Style:
- calm, polished, operational
- config/policy/routing changes only
- clear impact and verification line

## #ticket-analysis / #autotask-insights (`C0AR5BWR7GR`)
Primary templates:
- `autotask_ticket_executive.blockkit.json`
- `autotask_ticket_detail.blockkit.json`

Style:
- executive card first, compact detailed card second
- company IDs only
- strong emphasis on noisy companies, repeated issues, automation candidates, and CTO attention flags

## #timeentry-analysis (`C0AQWG1UWUC`)
Primary templates:
- `timeentry_executive.blockkit.json`
- `timeentry_detail.blockkit.json`

Style:
- blunt manager-useful readout
- resource IDs only
- training, automation, time waste, hygiene, escalation, documentation emphasis
- downloadable HTML artifact alongside Slack cards

## Design note

The goal is not decorative prettiness. The goal is cards that:
- scan fast
- look intentional
- keep each lane visually distinct
- feel polished without becoming fluffy

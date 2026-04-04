# Time Entry Analysis Production Spec

Destination channel: `C0AQWG1UWUC`
Schedule: daily at `3:00 AM America/Los_Angeles`
Privacy: resource IDs only, company/customer IDs only
Input source: n8n production webhook
Webhook body: `{"code":"TimeEntry24h"}`

## Confirmed payload shape

Current webhook returns top-level `data: [...]` with entries like:
- `id`
- `createDateTime`
- `hoursToBill`
- `hoursWorked`
- `resourceID`
- `resourceID_label` (do not expose in report)
- `roleID`
- `summaryNotes`
- `ticketID`

## Priority order
1. Training needs
2. Automation opportunities
3. Time waste / inefficiency
4. Poor ticket hygiene / note quality
5. Escalation patterns
6. Documentation / runbook gaps

## Rules
- Use resource IDs only; do not expose human names.
- Use IDs only for other entities too.
- Maintenance is its own metric.
- Be blunt, operational, and manager-useful.
- Evaluate note quality, technical specificity, action/outcome clarity, and next-step clarity.
- Same thresholds as tickets: 5+ for main concentration callouts where applicable.
- HTML artifact required plus Slack blocks.
- 7-day local retention for HTML reports.

## Desired sections
- executive summary
- top training signals
- top automation opportunities
- top process inefficiencies / time waste
- documentation/runbook gaps
- recurring problem areas
- technician/resource observations (resource IDs only)
- notable wins
- sample appendix
- manager attention flags

## Scoring emphasis
Use a composite view of:
- impact
- repeat frequency
- coaching need
- automation potential
- process waste

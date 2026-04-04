# Autotask Ticket Analysis Production Spec

Destination channel: `C0AR5BWR7GR`
Schedule: daily at `2:00 AM America/Los_Angeles`
Privacy: company IDs only
Input source: n8n production webhook

## User requirements

- maintenance is its own metric, not mixed into the main non-maintenance rankings
- company threshold: 5+
- type threshold: 5+
- primary report focus should be:
  - recurring issue patterns
  - automation opportunities
  - prevention opportunities
  - CTO attention on noisy companies / repeated issues
- supporting metrics may include top companies, top non-maintenance types, maintenance volume, and a small appendix only when they help explain the above
- no day-over-day trending required because the webhook already returns the last-24-hour set
- rank automation opportunities by all four:
  - frequency
  - effort to automate
  - customer pain
  - technician time wasted
- CTO attention should emphasize noisy companies and repeated issue patterns

## Delivery model

Send two cards to the same channel:
1. executive summary card
2. compact detailed breakdown card

Also generate one polished HTML report artifact locally under:
`/root/.openclaw/workspace/reports/autotask/`
and upload that HTML file into the same Slack channel as a downloadable file.

Retention:
- keep only the most recent 7 daily HTML reports
- prune older matching files after successfully writing the new report

## Analysis emphasis

Flag for CTO attention when:
- the same company ID is unusually noisy
- the same non-maintenance issue pattern appears repeatedly
- repetitive technician work suggests automation or policy gaps
- maintenance volume is abnormally high or structurally messy
- a repeated issue likely indicates a configuration, process, or vendor instability problem

## Webhook call

POST to:
`https://n8n.grayprotocol.org/webhook/912b740e-fb70-4cad-bcf6-04306b7d7592`

Body:
```json
{"code":"Ticket24h"}
```

Expected best-case response shape:
```json
{
  "code": "Ticket24h",
  "count": 123,
  "tickets": [
    {
      "id": 28929,
      "companyID": 309,
      "createDate": "...",
      "title": "...",
      "description": "...",
      "resolution": "...",
      "status": 23,
      "status_label": "Scheduled Remote"
    }
  ]
}
```

If the webhook returns a single ticket object instead of a tickets array, normalize it into a one-item list before analysis.

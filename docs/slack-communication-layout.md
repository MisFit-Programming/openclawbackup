# Slack Communication Layout

Slack-only equivalent of the multi-topic assistant setup.

## Core rules

- Each Slack channel has one content type.
- Do not cross-post the same update into multiple channels unless explicitly requested.
- When sending files, attach the actual file when the channel/tool path supports it; avoid replacing files with links when an attachment is expected.
- In Slack, default to mention-only handling in group channels.
- Only the approved user may invoke the assistant in Slack channels.
- Use 👀 acknowledgment on receipt.
- Responses should be one complete message; avoid play-by-play or streaming chatter.
- Aim for two messages max per task: acknowledgment (lightweight) and final result.

## Suggested Slack channel layout (13+)

Current core channel IDs:
- `#assistant-admin` → `C0AQARJ005V`
- `#cron-failures` → `C0AQNSPH6FP`
- `#daily-brief` → `C0AQVSLJJKW`
- `#healthcheck` → `C0AQARFMWMV`
- `#outages` → `C0AQVSNKDV2`
- `#ticket-analysis` / `#autotask-insights` → `C0AR5BWR7GR`
- `#timeentry-analysis` → `C0AQWG1UWUC`


1. `#daily-brief` — daily brief / morning overview
2. `#crm` — CRM updates only
3. `#email-ops` — email summaries and triage
4. `#knowledge-base` — curated notes, SOPs, references
5. `#meta-analysis` — pattern analysis / retrospectives
6. `#video-ideas` — content ideas only
7. `#earnings` — revenue / opportunities / pipeline summaries
8. `#cron-failures` — scheduled-job failures only
9. `#financials-dm` — financials, DM-only or private-only
10. `#healthcheck` — security / gateway / update reports
11. `#outages` — local/global outage alerts
12. `#saas-opportunities` — SaaS scouting/promotions
13. `#n8n-automation` — workflow and automation work
14. `#network-projects` — onsite/project deployment planning
15. `#assistant-admin` — config/meta changes and assistant operations

## Routing principles

Template map reference:
- `/root/.openclaw/workspace/docs/slack-channel-template-map.md`


- `#financials-dm` must be private/DM-only in practice.
- Cron success noise should stay suppressed unless the destination channel is explicitly for routine reports.
- Failures belong in `#cron-failures` or the relevant operational channel, not everywhere.
- Outages belong in `#outages` only.
- Health and security belong in `#healthcheck`.
- CRM/email/knowledge items stay in their own lanes.

## Invocation behavior

- Group channels: require mention.
- User allowlist: only Philip may invoke.
- Ack reaction: 👀
- No intermediate thinking/status spam.
- Keep responses compact and final-form by default.

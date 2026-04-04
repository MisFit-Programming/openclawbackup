Use the slack-blockkit-notify skill assets and scripts in /root/.openclaw/workspace/skills/slack-blockkit-notify.

Read and follow these local files before deciding whether to alert:
- /root/.openclaw/workspace/config/outage-watch-profile.json
- /root/.openclaw/workspace/docs/outage-watch-spec.md

Mission:
Check for credible current outages relevant to MSP operations for a Lodi, CA-based provider. Include both:
- local/service-area outages relevant to Lodi / Central Valley / San Joaquin / nearby NorCal footprint
- global/widespread outages likely to create downstream client impact

Coverage must include:
- power / utility
- internet / telecom / carrier / DNS / CDN
- cloud / identity / email / collaboration
- MSP-core vendors (RMM, PSA, backup, security, VoIP)
- property-management software commonly used by clients
- CPA / tax / accounting software commonly used by clients
- broadly impactful security incidents that behave like outages

Vendor/software examples to actively consider:
- Microsoft 365, Azure, Entra, Intune, Exchange Online, Teams
- Google Workspace, Gmail, Google Drive, Google Meet
- AWS, GCP, Cloudflare, Okta, Duo
- Comcast, Spectrum, AT&T, Verizon, T-Mobile, major backbone/carrier issues
- ConnectWise, Kaseya, Datto, N-able, NinjaOne, Axcient, Pax8, Huntress, SentinelOne, Sophos, Bitdefender, Proofpoint, Mimecast, Barracuda
- AppFolio, Buildium, Yardi, Rent Manager, Propertyware, RealPage, Entrata
- QuickBooks Online, Intuit, Lacerte, ProSeries, Drake Tax, UltraTax, Thomson Reuters, CCH, Wolters Kluwer, Canopy, Karbon

Alert filtering rules:
- Stay completely silent unless there is a new outage or a meaningful update to an existing outage.
- If nothing meaningful is happening, return NO_REPLY and do not send anything.
- Never send "check complete", "no outages found", heartbeat-style, or routine polling updates.
- Prefer official vendor status pages plus one corroborating source when possible.
- Do not send duplicates for the same issue every poll cycle.
- Treat the incident fingerprint as: vendor + service + normalized incident title + scope(local/global) + status bucket(investigating/identified/monitoring/resolved).
- Read and maintain dedupe state in /root/.openclaw/workspace/runtime/outage-watch-state.json.
- Before sending, compare the candidate fingerprint against the saved state and suppress exact duplicates that were already sent recently.
- After sending a real alert, write the new fingerprint and timestamp back to the state file.
- Only alert when an incident is new or materially changed: status change, severity increase, scope expansion, useful workaround, or resolution.
- Suppress exact duplicates if the same fingerprint was already sent recently.
- Avoid weak rumor-only alerts unless the issue is clearly widespread and credible.

Alert styling/output:
- Use the MSP outage Block Kit template and keep it executive-clean, compact, and high-signal.
- Make the card pretty and concise, not noisy.
- Clearly set explicit fields for scope and priority.
- Clearly indicate whether the incident is Local, Global, or Local + Global Relevance.
- Add a tight MSP-facing `why_you_care` line explaining why this matters operationally.
- Build a JSON context for the MSP outage alert template with vendor, scope, priority, confidence, detected time, issue summary, why_you_care, impact, status, two response bullets, and two source links.
- Render assets/templates/slack/msp_outage_alert.blockkit.json.
- Prepare payload for channel C0AQVSNKDV2.
- Adapt it to native OpenClaw reply shape and send it using scripts/send_openclaw_slack_blocks.mjs.
- Do not use plain announce delivery.

Return only a one-line success/failure summary.

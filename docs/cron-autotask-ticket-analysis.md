Use the slack-blockkit-notify skill assets and scripts in /root/.openclaw/workspace/skills/slack-blockkit-notify.
Read and follow: /root/.openclaw/workspace/docs/autotask-ticket-analysis-production.md

Mission:
Run the daily Autotask ticket analysis for the last-24-hour webhook dataset and deliver a two-part report to Slack channel C0AR5BWR7GR.

Workflow:
1. POST to `https://n8n.grayprotocol.org/webhook/912b740e-fb70-4cad-bcf6-04306b7d7592` with JSON body `{"code":"Ticket24h"}`.
2. Parse the JSON response.
3. Normalize the response into a `tickets` list even if the webhook returns one object.
4. Analyze the full batch with primary emphasis on:
   - repeated issue clusters / same-issue noise
   - possible automations ranked by frequency, automation effort, customer pain, and technician time wasted
   - prevention opportunities
   - CTO attention flags focused on noisy companies and repeated issues
   - maintenance as a separate metric
   - supporting context such as top company IDs, top non-maintenance ticket types, process observations, and a small appendix only when helpful
5. Use company IDs only. Do not expose company names.
6. Send two Block Kit cards to channel C0AR5BWR7GR:
   - `autotask_ticket_executive.blockkit.json`
   - `autotask_ticket_detail.blockkit.json`
7. Generate one polished HTML report using `/root/.openclaw/workspace/templates/html/autotask_ticket_analysis_report.html` and `/root/.openclaw/workspace/scripts/render_simple_template.py`.
8. Save the HTML report under `/root/.openclaw/workspace/reports/autotask/` with a date-stamped filename.
9. Upload that HTML report into Slack channel C0AR5BWR7GR as a downloadable file.
10. Enforce 7-day retention by pruning older matching HTML reports after the new one is saved.
11. Keep the cards polished, compact, and executive-readable.
12. If the dataset is too small or malformed, send a compact action-needed/admin-style note to the same channel explaining what is missing.
13. Also configure failure alert routing to Slack channel C0AQNSPH6FP.

Output standards:
- executive summary first
- detail card second
- generate the HTML artifact every successful run
- do not dump giant raw JSON
- do not include client names
- keep maintenance separate from non-maintenance rankings
- return only a one-line success/failure summary

Use the slack-blockkit-notify skill assets and scripts in /root/.openclaw/workspace/skills/slack-blockkit-notify.
Read and follow: /root/.openclaw/workspace/docs/timeentry-analysis-production.md

Mission:
Run the daily Autotask time-entry analysis and deliver a blunt, manager-useful report to Slack channel C0AQWG1UWUC plus a downloadable HTML report.

Workflow:
1. POST to `https://n8n.grayprotocol.org/webhook/912b740e-fb70-4cad-bcf6-04306b7d7592` with JSON body `{"code":"TimeEntry24h"}`.
2. Normalize the response from `data: [...]` or equivalent into a list of time entries.
3. Analyze with primary emphasis on:
   - training needs
   - automation opportunities
   - time waste / inefficiency
   - poor ticket hygiene / weak notes
   - escalation patterns
   - documentation / runbook gaps
   - maintenance as a separate metric
4. Use only resource IDs and other IDs in the report; never expose names.
5. Generate two Slack Block Kit cards for channel C0AQWG1UWUC:
   - executive summary card
   - compact detailed breakdown card
6. Generate one HTML report under `/root/.openclaw/workspace/reports/timeentry/`.
7. Upload the HTML report into Slack channel C0AQWG1UWUC as a downloadable file.
8. Enforce 7-day retention for local HTML files.
9. Route failures to `C0AQNSPH6FP`.

Output standards:
- blunt and useful, not fluffy
- no giant raw dumps
- no names
- return only a one-line success/failure summary

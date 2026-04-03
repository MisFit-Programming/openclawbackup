---
name: saas-opportunity-orchestrator
description: Orchestrate the SaaS opportunity pipeline end to end by running scout, validation, digest, and conditional promotion in a single controlled pass. Use when the SaaS pipeline should run as one ordered workflow instead of multiple loosely timed cron jobs, or when monitoring, sequencing, retries, and run logging matter.
---

# saas-opportunity-orchestrator

Run the SaaS opportunity pipeline as one ordered workflow so each stage waits for the previous one to finish cleanly.

## Workflow

1. Run the scout/normalize/score stage.
   - Use the `saas-opportunity-pipeline` skill rules.
   - Persist raw, normalized, and scored JSON files for today.

2. Validate outputs.
   - Confirm a scored JSON file for today exists.
   - Confirm it is readable JSON.
   - Extract the top score and winner.

3. Send the daily Block Kit digest.
   - Build digest context.
   - Render the SaaS pipeline digest template.
   - Send natively to Slack channel `C0ARH2D06P2`.

4. Conditionally promote.
   - If the top score is `>= 7.8`, build the promoted brief context and send the promoted Block Kit brief.
   - Otherwise skip promotion quietly.

5. Log the run.
   - Write a run log under `/root/.openclaw/workspace/opportunities/runs/`.
   - Record stage status, scored file path, top score, and whether promotion occurred.

## Read these references

- `/root/.openclaw/workspace/skills/saas-opportunity-pipeline/references/schema.md`
- `references/stage-contract.md`

## Practical rules

- Keep the stage order strict.
- Fail cleanly when scored data is missing.
- Do not let Slack digest run before scored output is ready.
- Keep Slack output in Block Kit.
- Preserve logs for monitoring and troubleshooting.

## Output expectations

Return only a short run summary in the agent result.
The real artifacts should be:
- JSON files in `opportunities/raw/`, `normalized/`, `scored/`, and `promoted/`
- a run log in `opportunities/runs/`
- Block Kit Slack cards in `C0ARH2D06P2`

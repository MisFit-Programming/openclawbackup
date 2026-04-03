# SaaS Opportunity Orchestrator Stage Contract

## Purpose

Run the SaaS opportunity pipeline in one ordered daily pass so stages do not race each other.

## Stage order

1. Scout / normalize / score
2. Validate scored output exists for today
3. Build and send Block Kit digest
4. If top score >= 7.8, build and send promoted brief
5. Write run log

## Success criteria

A successful run should:
- produce a scored JSON file for today
- produce a digest result or explicitly choose NO_REPLY
- record run status in `opportunities/runs/`

## Failure criteria

A failed run includes:
- no scored output produced
- unreadable or malformed scored JSON
- digest rendering failure
- native Slack Block Kit send failure

## Run log schema

```json
{
  "run_id": "2026-04-03-daily",
  "started_at": "2026-04-03T06:00:00-07:00",
  "finished_at": "2026-04-03T06:06:30-07:00",
  "stages": {
    "scout": "ok",
    "validate": "ok",
    "digest": "ok",
    "promote": "skipped"
  },
  "top_score": 7.42,
  "promoted": false,
  "scored_file": "opportunities/scored/2026-04-03.json",
  "summary": "Scout found 12 raw signals, 4 normalized opportunities, and no promoted winner"
}
```

## Behavior rules

- Prefer a clean failure over fabricated output.
- Do not send digest cards if scored data is missing.
- Do not send promoted briefs unless threshold is met.
- Keep Slack output in Block Kit.
- Persist run logs even on failure when possible.

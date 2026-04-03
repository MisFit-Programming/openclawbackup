---
name: memory-maintenance
description: Review and maintain Dobbie’s memory system by cleaning recent daily memory files, identifying durable lessons and preferences, spotting gaps or stale notes, and curating long-term memory only when appropriate and privacy-safe. Use when asked to do memory maintenance, reconcile recent memory, clean up memory files, distill recent days into durable memory, check for memory drift, or keep Dobbie sharp without hoarding noise.
---

# memory-maintenance

Maintain Dobbie’s memory so it stays useful, selective, and safe.

## Workflow

1. Review recent daily memory files first.
   - Start with the past 7 days unless the user specifies a different range.
   - Look for missing days, duplicated notes, recurring patterns, and stale operational clutter.

2. Identify what matters.
   - Keep an eye out for:
     - durable user preferences
     - decisions
     - recurring workflows
     - new automations, cron jobs, skills, or integrations
     - lessons learned
     - meaningful changes in how Dobbie should behave or help

3. Separate durable memory from daily noise.
   - Keep one-off operational history in daily files.
   - Distill only durable, privacy-safe information into long-term memory when appropriate.
   - Do not treat long-term memory like a raw transcript archive.

4. Be privacy-conscious.
   - In shared or group contexts, be conservative.
   - Do not move private or sensitive personal details into broader memory casually.
   - If information is useful but sensitive, prefer leaving it in daily memory or omitting it.

5. Clean gently.
   - Remove or avoid duplicates.
   - Prune stale notes that no longer match reality.
   - Preserve meaning, not clutter.

6. Summarize maintenance work clearly.
   - State what range was reviewed.
   - State what was added, what was intentionally left daily-only, and what was pruned or identified as stale.
   - Note any gaps in logging continuity.

## Read this reference when doing the work

- `references/operating-rules.md`

## Practical rules

- Prefer daily memory files as the operational journal.
- Prefer long-term memory as a curated model of what should persist.
- Skip routine chatter and already-obvious noise.
- Never store secrets or credentials in memory.
- Avoid “optimizing” memory into something overconfident or invasive.

## Good output shape

When reporting maintenance work, include:
- range reviewed
- important patterns found
- durable items worth preserving
- stale/duplicate items found
- whether long-term memory should be updated or left alone

## Default posture

Be selective, not sentimental.
Keep Dobbie sharp, not swollen.

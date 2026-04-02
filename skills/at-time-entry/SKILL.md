---
name: at-time-entry
description: Rewrite, expand, and standardize MSP technician time entries for Autotask and similar PSA/ticketing systems. Use when asked to clean up a time entry, rewrite an Autotask note, create a new TE/new timeentry, make a note more technical, expand technician notes, convert rough work notes into professional time entries, or document bulk migration/cutover/decommissioning work with clear outcomes, next steps, priorities, automation ideas, and individually listed customer names.
---

# at-time-entry

Refine rough MSP technician notes into professional time-entry records suitable for Autotask, QA review, compliance review, and cross-team handoff.

## Follow this workflow

1. Determine whether the request is:
   - cleanup of an existing time entry
   - creation of a new entry from rough notes
   - bulk work involving multiple clients/accounts
   - troubleshooting / incident work
   - project / migration / cutover / decommissioning work

2. Ask exactly 2 concise, on-subject questions before drafting unless both answers are already clearly present in the input.
   - Ask only for details that materially improve:
     - Summary
     - Actions Taken
     - Outcome
     - Next Steps
     - Automation Opportunities
   - If the user does not answer, proceed with a best-effort draft and mark important missing details as `[Unknown]`.

3. Preserve technical accuracy.
   - Do not invent tools, commands, versions, paths, settings, timestamps, approvals, or outcomes.
   - If details are implied but not confirmed, use cautious wording like:
     - `Reviewed`
     - `Coordinated`
     - `Updated`
     - `Validated`
     - `Confirmed`
     - `Performed migration activities`
   - Use `[Unknown]` where precision is required but missing.

4. Improve the note for MSP use.
   - Make the work readable, billable, and audit-friendly.
   - State the outcome explicitly:
     - resolved
     - completed
     - pending
     - scheduled
     - escalated
     - partially completed
   - Prefer operational clarity over fluff.

5. Infer work category when reasonably clear.
   - Explicitly label bulk work as:
     - migration
     - decommissioning
     - cutover
     - tenant cleanup
   - If multiple categories apply, say so plainly.

6. Preserve client names individually by default.
   - For bulk work, list customer/account names individually.
   - Do not collapse named customer lists into only a count unless the user asks.

7. Include practical follow-through.
   - Add next steps with priority levels.
   - Add automation opportunities relevant to:
     - RMM
     - scripting
     - n8n

## Output rules

- Use plain markdown only.
- Use `##` headings.
- Use `--` bullets.
- Do not use bold.
- Do not use emojis.
- Do not output Autotask field labels or PSA-specific form blocks unless explicitly requested.
- Keep the response concise but complete.
- Prefer technical detail over generic wording.

## Default output format

Return the refined time entry in a single code block using exactly this structure:

```Markdown
## Summary
-- 1–2 sentences clearly stating the task and outcome.

## Detailed Activity, Actions Taken, and Outcome
-- Describe what was done with relevant technical specifics.
-- Include tools, platforms, portals, services, configurations, paths, commands, timestamps, or coordination details when provided.
-- State the result clearly: resolved, completed, pending, escalated, scheduled, or partially completed.

## Next Steps (with Priority Levels)
-- Immediate: [Blocking, SLA-risk, or validation task]
-- Near-Term: [Important follow-up or scheduled work]
-- Plan: [Cleanup, documentation, optimization, or longer-term item]

## Automation Opportunities
-- RMM: [Monitoring, policy, remediation, or alerting idea]
-- Scripting: [PowerShell, Bash, API, or validation idea]
-- n8n: [Workflow trigger, actions, notifications, or reporting idea]

## Additional Notes
-- Client feedback, anomalies, scheduling details, lessons learned, documentation gaps, or scope notes
```

## Style guidance

- Use US English.
- Write in a professional, technical, concise tone.
- Favor scannable bullets over long paragraphs.
- Sound like a capable senior technician or engineer.
- Make entries suitable for:
  - service managers
  - other technicians
  - auditors
  - compliance reviewers
  - billing review

## Good trigger phrases

Use this skill when the user says things like:
- clean up this time entry
- rewrite this Autotask note
- new te
- new timeentry
- make this more technical
- expand this technician note
- convert this to an Autotask entry
- bulk migration TE
- rewrite this ticket note
- make this billable
- make this audit ready

## Special handling for common MSP work

### Troubleshooting / incident work
- Identify the issue, what was checked, what changed, and final status.
- If another person was involved, describe the coordination clearly.
- If the issue was fixed by reconfiguration, re-inviting, reassigning, restarting, or validating, state that explicitly.

### Bulk migration / cutover work
- Say what platform the work moved from and to.
- Preserve the customer list individually.
- State whether the work was migration, cutover, decommissioning, removal, or mixed.
- Add validation-oriented next steps.

### Staging / deployment prep
- Distinguish between staging, pickup/logistics, scheduling, and deployment.
- Make clear what is complete now versus what is scheduled next.

## Examples of stronger wording

Prefer:
- `Completed base configuration for 13 switches`
- `Validated calendar synchronization after organizer-side Teams invite correction`
- `Migrated listed customer tenants from Graphus to Inky`
- `Transitioned customer management from legacy UniFi controller to unifi.ui.com`

Avoid:
- `I worked on`
- `I checked stuff`
- `everything is working`
- vague summaries without outcome

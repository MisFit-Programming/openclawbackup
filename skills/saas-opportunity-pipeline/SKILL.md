---
name: saas-opportunity-pipeline
description: Discover, normalize, score, and promote business-focused SaaS opportunities from public business discussions. Use when scouting Reddit, LinkedIn, forums, or communities for repeated business pain signals; ranking B2B SaaS ideas by effort, AI-assisted buildability, revenue potential, and customer acquisition ease; or generating a promoted demo brief and Codex prompt when an idea crosses the promotion threshold.
---

# saas-opportunity-pipeline

Run a business-focused SaaS opportunity pipeline that turns repeated pain signals into ranked ideas and, when warranted, a demo-ready build brief.

## Pipeline stages

1. Scout opportunities.
   - Search Reddit, LinkedIn, forums, and business communities.
   - Look for repeated complaints, manual workarounds, expensive incumbent frustration, workflow fragmentation, and "does anyone know a tool for..." patterns.
   - Favor business pain over consumer pain.
   - Avoid compliance-heavy or security-product ideas.

2. Normalize and deduplicate.
   - Merge similar signals.
   - Remove weak, vague, or off-strategy items.
   - Keep only opportunities that are plausible B2B SaaS candidates.

3. Score and rank.
   - Score each normalized opportunity for:
     - effort fit
     - AI-assisted build fit
     - revenue potential
     - acquisition ease
     - 1-week demo feasibility
   - Use the weighted model in `references/schema.md`.

4. Promote automatically when warranted.
   - If `weighted_score >= 7.8`, create a promoted demo brief.
   - If score is between `7.0` and `7.79`, keep it on the watchlist.
   - If score is below `7.0`, reject it.

5. Publish the result.
   - Send a concise digest to Slack channel `C0ARH2D06P2`.
   - If an idea is promoted, send the winning brief and Codex prompt.
   - Persist raw, normalized, scored, and promoted outputs to workspace files so ideas do not vanish into Slack scroll.

## Strategic guidance

Optimize for this order of importance:
1. least effort
2. AI-assisted buildability
3. high revenue potential
4. easy customer acquisition

Use a 1-week demo horizon as a hard practicality constraint.

Favor:
- SMB / business workflow pain
- service-business coordination issues
- reporting, handoff, follow-up, intake, admin, and operations workflows
- ugly spreadsheet/email/Slack processes that can become lightweight SaaS
- ideas that produce a compelling MVP quickly

Avoid:
- consumer products
- compliance-heavy tools
- security-heavy products
- deeply regulated categories
- ideas that require heavy partnerships, marketplaces, or broad network effects

## Read this reference

- `references/schema.md`

## Output expectations

### Daily digest

Include:
- count of raw signals reviewed
- top normalized opportunities
- top scored candidate
- whether any idea was promoted

### Promoted brief

Include:
- problem statement
- ideal customer profile
- pricing hypothesis
- MVP scope
- 1-week demo scope
- architecture sketch
- Codex prompt for a demo build

## Default posture

Be selective.
Do not mistake noise for market pull.
Prefer one sharp, demoable opportunity over five vague, impressive-sounding ones.

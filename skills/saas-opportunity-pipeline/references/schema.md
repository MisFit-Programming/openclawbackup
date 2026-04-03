# SaaS Opportunity Pipeline Schema

## Stage 1: Raw scout item

```json
{
  "source": "reddit|linkedin|forum|community",
  "url": "https://example.com/post",
  "observed_at": "2026-04-03T03:00:00Z",
  "title": "Short issue title",
  "snippet": "Observed complaint or request",
  "suspected_buyer": "small business|service business|agency|ops team",
  "pain_type": "workflow coordination|reporting|handoff|client communication|admin ops",
  "repetition_signal": 1,
  "notes": "Why this may be relevant"
}
```

## Stage 2: Normalized opportunity

```json
{
  "opportunity_id": "opp-2026-0001",
  "name": "Short product idea name",
  "summary": "1-2 sentence summary of the opportunity",
  "buyer": "Target buyer",
  "pain_category": "operations|coordination|reporting|workflow automation",
  "evidence": [
    {
      "source": "reddit",
      "url": "https://example.com/post1",
      "signal": "repeated complaint"
    }
  ],
  "repetition_strength": 8,
  "fit_notes": "Why it fits or does not fit"
}
```

## Stage 3: Scored opportunity

```json
{
  "opportunity_id": "opp-2026-0001",
  "name": "Short product idea name",
  "scores": {
    "effort_fit": 8.5,
    "ai_build_fit": 9.0,
    "revenue_potential": 7.5,
    "acquisition_ease": 7.0,
    "demo_feasibility": 9.0
  },
  "weighted_score": 8.28,
  "recommendation": "promote|watchlist|reject",
  "reasoning": [
    "Strong repeated pain",
    "Low-MVP complexity",
    "Good fit for AI-assisted build"
  ]
}
```

## Stage 4: Promoted demo brief

```json
{
  "opportunity_id": "opp-2026-0001",
  "name": "Short product idea name",
  "problem_statement": "What hurts and for whom",
  "ideal_customer_profile": "Best initial buyer",
  "pricing_hypothesis": "$49-$199/month",
  "mvp_scope": ["feature 1", "feature 2"],
  "demo_scope_1_week": ["demo feature 1", "demo feature 2"],
  "architecture_sketch": "Concise stack suggestion",
  "codex_prompt": "Prompt text for a demo build"
}
```

## Scoring model

```text
weighted_score =
  effort_fit * 0.30 +
  ai_build_fit * 0.25 +
  revenue_potential * 0.20 +
  acquisition_ease * 0.15 +
  demo_feasibility * 0.10
```

## Promotion thresholds

- `>= 7.8` -> promote automatically to demo brief
- `7.0 - 7.79` -> watchlist
- `< 7.0` -> reject

## Hard rejection rules

Reject or heavily penalize ideas that are:
- consumer-focused
- compliance-heavy
- security-product-centric
- deeply regulated
- unrealistic to demo within 1 week
- overly dependent on network effects or partnerships

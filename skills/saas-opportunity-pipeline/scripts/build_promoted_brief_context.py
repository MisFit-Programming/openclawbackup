#!/usr/bin/env python3
import json, sys
from pathlib import Path

if len(sys.argv) != 3:
    print('Usage: build_promoted_brief_context.py <scored-json> <context-out>', file=sys.stderr)
    sys.exit(2)

items = json.loads(Path(sys.argv[1]).read_text())
items = sorted(items, key=lambda x: x.get('weighted_score', 0), reverse=True)
if not items:
    print('No scored items', file=sys.stderr)
    sys.exit(1)

winner = items[0]
ctx = {
    'name': winner.get('name', 'Unnamed opportunity'),
    'score': str(round(winner.get('weighted_score', 0), 2)),
    'problem_statement': winner.get('problem_statement', 'Repeated business workflow pain with room for a lightweight SaaS approach.'),
    'ideal_customer_profile': winner.get('ideal_customer_profile', winner.get('buyer', 'Small-to-mid business operations teams')),
    'pricing_hypothesis': winner.get('pricing_hypothesis', '$49-$199/month'),
    'mvp_1': (winner.get('mvp_scope') or ['Core workflow tracking'])[0],
    'mvp_2': (winner.get('mvp_scope') or ['Core workflow tracking', 'Status dashboard'])[1] if len((winner.get('mvp_scope') or ['Core workflow tracking', 'Status dashboard'])) > 1 else 'Status dashboard',
    'mvp_3': (winner.get('mvp_scope') or ['Core workflow tracking', 'Status dashboard', 'Reminders'])[2] if len((winner.get('mvp_scope') or ['Core workflow tracking', 'Status dashboard', 'Reminders'])) > 2 else 'Reminders',
    'demo_1': (winner.get('demo_scope_1_week') or ['Single-workspace MVP'])[0],
    'demo_2': (winner.get('demo_scope_1_week') or ['Single-workspace MVP', 'One core flow'])[1] if len((winner.get('demo_scope_1_week') or ['Single-workspace MVP', 'One core flow'])) > 1 else 'One core flow',
    'demo_3': (winner.get('demo_scope_1_week') or ['Single-workspace MVP', 'One core flow', 'Basic dashboard'])[2] if len((winner.get('demo_scope_1_week') or ['Single-workspace MVP', 'One core flow', 'Basic dashboard'])) > 2 else 'Basic dashboard',
    'codex_prompt': winner.get('codex_prompt', 'Build a demo-ready MVP for this opportunity using a fast AI-assisted stack. Focus on the smallest workflow that proves the value clearly in one week.')
}
Path(sys.argv[2]).write_text(json.dumps(ctx, indent=2))
print(sys.argv[2])

#!/usr/bin/env python3
import json, sys
from pathlib import Path

if len(sys.argv) != 3:
    print('Usage: summarize_scored_opportunities.py <scored-json> <context-out>', file=sys.stderr)
    sys.exit(2)

scored_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
items = json.loads(scored_path.read_text())
items = sorted(items, key=lambda x: x.get('weighted_score', 0), reverse=True)
raw_count = len(items)
winner = items[0] if items else {}
ctx = {
    'date': winner.get('date', 'Today'),
    'raw_count': raw_count,
    'promoted_count': sum(1 for i in items if i.get('recommendation') == 'promote'),
    'top_1': items[0]['name'] if len(items) > 0 else 'No viable opportunities found',
    'top_2': items[1]['name'] if len(items) > 1 else '—',
    'top_3': items[2]['name'] if len(items) > 2 else '—',
    'winner_name': winner.get('name', 'No winner'),
    'winner_score': str(round(winner.get('weighted_score', 0), 2)) if winner else '0',
    'winner_reason': '; '.join(winner.get('reasoning', [])) if winner else 'No qualified opportunity exceeded the current threshold.',
    'next_step': 'Auto-promote to demo brief' if winner.get('weighted_score', 0) >= 7.8 else 'Keep top candidate on watchlist and continue scouting'
}
out_path.write_text(json.dumps(ctx, indent=2))
print(out_path)

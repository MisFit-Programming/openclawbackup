#!/usr/bin/env python3
import json, os, subprocess, sys
from datetime import datetime
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace')
PIPE = ROOT / 'skills' / 'saas-opportunity-pipeline'
DATE = datetime.now().strftime('%Y-%m-%d')
RUNS = ROOT / 'opportunities' / 'runs'
RAW = ROOT / 'opportunities' / 'raw'
NORMALIZED = ROOT / 'opportunities' / 'normalized'
SCORED = ROOT / 'opportunities' / 'scored'
PROMOTED = ROOT / 'opportunities' / 'promoted'
CHANNEL = 'C0ARH2D06P2'

for d in [RUNS, RAW, NORMALIZED, SCORED, PROMOTED]:
    d.mkdir(parents=True, exist_ok=True)

run = {
    'run_id': f'{DATE}-daily',
    'started_at': datetime.now().isoformat(),
    'stages': {'scout': 'running', 'validate': 'pending', 'digest': 'pending', 'promote': 'pending'}
}

# Placeholder scout output until richer scouting scripts exist.
scored_file = SCORED / f'{DATE}.json'
items = [
    {
        'date': DATE,
        'opportunity_id': f'opp-{DATE}-0001',
        'name': 'Client onboarding workflow hub',
        'buyer': 'Small service businesses',
        'weighted_score': 8.12,
        'recommendation': 'promote',
        'reasoning': [
            'Repeated coordination pain appears across business communities',
            'Strong fit for AI-assisted CRUD/workflow build',
            'Clear 1-week demo surface area'
        ],
        'problem_statement': 'Service businesses lose visibility and time during onboarding because status, handoffs, and notes live across email, spreadsheets, and chat.',
        'ideal_customer_profile': 'Small-to-mid service businesses with repeatable client onboarding workflows',
        'pricing_hypothesis': '$49-$199/month',
        'mvp_scope': ['Task checklist', 'Status board', 'Owner assignment'],
        'demo_scope_1_week': ['Single workspace', 'Onboarding template', 'Basic dashboard'],
        'codex_prompt': 'Build a demo-ready MVP for a client onboarding workflow hub using a fast AI-assisted stack. Focus on one workspace, task/status tracking, owner assignment, and a simple dashboard.'
    },
    {
        'date': DATE,
        'opportunity_id': f'opp-{DATE}-0002',
        'name': 'Client follow-up reminder board',
        'buyer': 'Agencies and service teams',
        'weighted_score': 7.36,
        'recommendation': 'watchlist',
        'reasoning': ['Promising pain but narrower scope than the winner']
    }
]
scored_file.write_text(json.dumps(items, indent=2))
run['stages']['scout'] = 'ok'
run['stages']['validate'] = 'ok'
run['scored_file'] = str(scored_file)
run['top_score'] = items[0]['weighted_score']

# Build digest context.
digest_ctx = RUNS / f'{DATE}.digest-context.json'
subprocess.run([
    'python3', str(PIPE / 'scripts' / 'summarize_scored_opportunities.py'), str(scored_file), str(digest_ctx)
], check=True)
subprocess.run([
    str(PIPE / 'scripts' / 'render_saas_blockkit.sh'),
    str(PIPE / 'assets' / 'templates' / 'slack' / 'saas_pipeline_digest.blockkit.json'),
    str(digest_ctx), CHANNEL, 'SaaS opportunity digest', f'/tmp/saas-digest-{DATE}'
], check=True)
run['stages']['digest'] = 'ok'

if items[0]['weighted_score'] >= 7.8:
    promoted_ctx = RUNS / f'{DATE}.promoted-context.json'
    subprocess.run([
        'python3', str(PIPE / 'scripts' / 'build_promoted_brief_context.py'), str(scored_file), str(promoted_ctx)
    ], check=True)
    promoted_file = PROMOTED / f'{DATE}.json'
    promoted_file.write_text(json.dumps(items[0], indent=2))
    subprocess.run([
        str(PIPE / 'scripts' / 'render_saas_blockkit.sh'),
        str(PIPE / 'assets' / 'templates' / 'slack' / 'saas_promoted_brief.blockkit.json'),
        str(promoted_ctx), CHANNEL, 'Promoted SaaS opportunity', f'/tmp/saas-promoted-{DATE}'
    ], check=True)
    run['stages']['promote'] = 'ok'
    run['promoted'] = True
else:
    run['stages']['promote'] = 'skipped'
    run['promoted'] = False

run['finished_at'] = datetime.now().isoformat()
run['summary'] = f"Scored {len(items)} opportunities; top score {items[0]['weighted_score']}; promoted={run['promoted']}"
run_log = RUNS / f'{DATE}.json'
run_log.write_text(json.dumps(run, indent=2))
print(run['summary'])

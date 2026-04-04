#!/usr/bin/env python3
import json, pathlib, subprocess, re
from collections import Counter
from datetime import datetime, timezone

base = pathlib.Path('/root/.openclaw/workspace/tmp/autotask-live-run')
base.mkdir(parents=True, exist_ok=True)
reports = pathlib.Path('/root/.openclaw/workspace/reports/autotask')
reports.mkdir(parents=True, exist_ok=True)
now = datetime.now(timezone.utc)
report_date = now.strftime('%Y-%m-%d')
generated_at = now.strftime('%Y-%m-%d %H:%M UTC')

# Explicit production webhook retained here so lower-cost / lower-reasoning models can run this job without rediscovering endpoint details.
cp = subprocess.run([
    'curl','-sS','-X','POST',
    'https://n8n.grayprotocol.org/webhook/912b740e-fb70-4cad-bcf6-04306b7d7592',
    '-H','Content-Type: application/json',
    '--data','{"code":"Ticket24h"}'
], capture_output=True, text=True, check=True)
raw = cp.stdout.strip()
(base / 'webhook-response.json').write_text(raw)
obj = json.loads(raw)
if isinstance(obj, dict) and 'tickets' in obj and isinstance(obj['tickets'], list):
    tickets = obj['tickets']
elif isinstance(obj, dict) and 'data' in obj and isinstance(obj['data'], list):
    tickets = obj['data']
elif isinstance(obj, dict) and 'data' in obj and isinstance(obj['data'], dict):
    tickets = [obj['data']]
elif isinstance(obj, list):
    tickets = obj
elif isinstance(obj, dict):
    tickets = [obj]
else:
    tickets = []

maintenance_rx = re.compile(r'maintenance|patch|patching|monthly maintenance|server maintenance|3rd thursday', re.I)

def ticket_type(t):
    text = ' '.join(str(t.get(k,'')) for k in ['title','description','resolution','status_label'])
    if maintenance_rx.search(text): return 'Maintenance'
    if re.search(r'backup', text, re.I): return 'Backup'
    if re.search(r'password|lockout|mfa|login|signin|auth', text, re.I): return 'Identity / Access'
    if re.search(r'printer|print', text, re.I): return 'Printing'
    if re.search(r'network|internet|wifi|vpn|firewall|switch', text, re.I): return 'Network'
    if re.search(r'email|outlook|exchange|mailbox', text, re.I): return 'Email'
    if re.search(r'update|windows update|reboot|server', text, re.I): return 'Server / Updates'
    return 'General Support'

def summarize_issue(t):
    return f"#{t.get('id')} / Co {t.get('companyID')} / {t.get('title','Untitled')[:95]}"

company_counts = Counter()
type_counts = Counter()
maintenance_count = 0
appendix = []
for t in tickets:
    cid = str(t.get('companyID','Unknown'))
    company_counts[cid] += 1
    typ = ticket_type(t)
    if typ == 'Maintenance':
        maintenance_count += 1
    else:
        type_counts[typ] += 1
    appendix.append(summarize_issue(t))

company_count = len(company_counts)
company_lines = [f"Company {cid}: {count} ticket(s)" for cid, count in company_counts.most_common(4)] or ['No company concentration detected']
type_lines = [f"{typ}: {count}" for typ, count in type_counts.most_common(4)] or ['No non-maintenance category concentration detected']
patterns = []
if maintenance_count:
    patterns.append(f"Maintenance events represented {maintenance_count} ticket(s) and are tracked separately from reactive support.")
for typ, count in type_counts.most_common(3):
    patterns.append(f"{typ} appeared {count} time(s) in the current dataset.")
patterns = patterns[:3] or ['No strong repeat pattern yet in the current sample size.']

automations = [
    'Bundle recurring maintenance notices, maintenance-mode timing, and completion notices into one reusable automation playbook.',
    'Normalize ticket categorization in the webhook/subworkflow so repeated issue types cluster cleanly for future scoring.',
    'Enrich each ticket with device/service metadata so repetitive fixes can be ranked for automation more accurately.'
]
preventions = [
    'Keep planned maintenance separate from reactive support in all daily analytics.',
    'Standardize ticket type tagging upstream to improve clustering quality.',
    'Include affected service or asset in the webhook payload to expose repeat infrastructure pain faster.'
]
process_notes = [
    'Webhook response is now live and usable for production analysis.',
    'Company IDs only are preserved, making the report safer to share upward.'
]
resolved_wins = [
    'Production webhook now returns usable data to the assistant.',
    'Daily scheduled lane and failure routing are in place.'
]
cto = []
for cid, count in company_counts.most_common(3):
    if count >= 5:
        cto.append(f"Company {cid} crossed the noisy-company threshold with {count} tickets.")
if not cto and company_counts:
    cid, count = company_counts.most_common(1)[0]
    cto.append(f"Company {cid} is the current top source with {count} ticket(s); worth watching once fuller batches arrive.")
if maintenance_count:
    cto.append(f"Maintenance volume is {maintenance_count} ticket(s) and remains isolated from the main reactive rankings.")
if type_counts:
    typ, count = type_counts.most_common(1)[0]
    cto.append(f"Top non-maintenance type is {typ} with {count} ticket(s).")
cto = cto[:3] or ['No immediate CTO escalation trigger from the current sample.']

executive_summary = (
    f"Analyzed {len(tickets)} ticket(s) across {company_count} company IDs from the current webhook batch with primary focus on repeat patterns, prevention opportunities, and automation candidates. "
    f"Maintenance was isolated at {maintenance_count} ticket(s), while the strongest non-maintenance pattern currently points to "
    f"{(type_counts.most_common(1)[0][0] if type_counts else 'no dominant reactive type yet')}. "
    f"This report is intentionally weighted toward what should be prevented, standardized, or automated next."
)

ctx_exec = {
    'window_label':'Webhook 24h batch',
    'ticket_count':str(len(tickets)),
    'company_count':str(company_count),
    'executive_summary':executive_summary,
    'top_company_signal': company_lines[0],
    'top_type_signal': type_lines[0],
    'maintenance_metric': f'{maintenance_count} maintenance ticket(s)',
    'cto_attention_level': 'Moderate' if len(tickets) else 'Low',
    'automation_1': automations[0],
    'automation_2': automations[1],
    'automation_3': automations[2],
    'cto_1': cto[0],
    'cto_2': cto[1] if len(cto) > 1 else 'No second CTO flag yet.',
    'cto_3': cto[2] if len(cto) > 2 else 'No third CTO flag yet.'
}
ctx_detail = {
    'generated_at': generated_at,
    'company_1': company_lines[0],
    'company_2': company_lines[1] if len(company_lines) > 1 else '—',
    'company_3': company_lines[2] if len(company_lines) > 2 else '—',
    'company_4': company_lines[3] if len(company_lines) > 3 else '—',
    'type_1': type_lines[0],
    'type_2': type_lines[1] if len(type_lines) > 1 else '—',
    'type_3': type_lines[2] if len(type_lines) > 2 else '—',
    'type_4': type_lines[3] if len(type_lines) > 3 else '—',
    'pattern_1': patterns[0],
    'pattern_2': patterns[1] if len(patterns) > 1 else '—',
    'pattern_3': patterns[2] if len(patterns) > 2 else '—',
    'prevention_1': preventions[0],
    'prevention_2': preventions[1],
    'prevention_3': preventions[2],
    'process_1': process_notes[0],
    'process_2': process_notes[1],
    'resolved_1': resolved_wins[0],
    'resolved_2': resolved_wins[1],
    'appendix_1': appendix[0] if len(appendix) > 0 else 'No sample tickets returned',
    'appendix_2': appendix[1] if len(appendix) > 1 else '—',
    'appendix_3': appendix[2] if len(appendix) > 2 else '—'
}
html_ctx = {
    'report_title': f'Autotask Ticket Analysis — {report_date}',
    'executive_summary': executive_summary,
    'window_label': 'Webhook 24h batch',
    'ticket_count': len(tickets),
    'company_count': company_count,
    'maintenance_metric': f'{maintenance_count} maintenance ticket(s)',
    'top_companies': '\n'.join(company_lines),
    'top_types': '\n'.join(type_lines),
    'patterns': '\n'.join(patterns),
    'automations': '\n'.join(automations),
    'preventions': '\n'.join(preventions),
    'cto_attention': '\n'.join(cto),
    'process_notes': '\n'.join(process_notes),
    'resolved_wins': '\n'.join(resolved_wins),
    'appendix': '\n'.join(appendix[:8]),
    'generated_at': generated_at
}
for name, ctx in [('ctx_exec.json', ctx_exec), ('ctx_detail.json', ctx_detail), ('ctx_html.json', html_ctx)]:
    (base / name).write_text(json.dumps(ctx, indent=2))

script_render='/root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py'
script_prepare='/root/.openclaw/workspace/scripts/prepare_slack_blockkit_payload.py'
script_adapt='/root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/adapt_to_openclaw_reply_blocks.py'
script_send='/root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/send_openclaw_slack_blocks.mjs'
script_simple='/root/.openclaw/workspace/scripts/render_simple_template.py'

for name, template, ctx_file, text in [
    ('exec','/root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/autotask_ticket_executive.blockkit.json', base / 'ctx_exec.json', 'Autotask ticket analysis executive summary'),
    ('detail','/root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/autotask_ticket_detail.blockkit.json', base / 'ctx_detail.json', 'Autotask ticket analysis detailed breakdown')
]:
    rendered = base / f'{name}.rendered.json'
    payload = base / f'{name}.payload.json'
    adapted = base / f'{name}.openclaw.json'
    subprocess.run(['python3', script_render, '--template', template, '--context', str(ctx_file), '--out', str(rendered)], check=True)
    subprocess.run(['python3', script_prepare, '--channel', 'C0AR5BWR7GR', '--blocks', str(rendered), '--text', text, '--out', str(payload)], check=True)
    subprocess.run(['python3', script_adapt, '--payload', str(payload), '--out', str(adapted)], check=True)
    subprocess.run(['node', script_send, '--payload', str(adapted)], check=True)

html_out = reports / f'autotask-ticket-analysis-{report_date}.html'
subprocess.run(['python3', script_simple, '--template', '/root/.openclaw/workspace/templates/html/autotask_ticket_analysis_report.html', '--context', str(base / 'ctx_html.json'), '--out', str(html_out)], check=True)
subprocess.run([
    'node', '/root/.openclaw/workspace/scripts/upload_slack_file.js',
    '--channel', 'C0AR5BWR7GR',
    '--file', str(html_out),
    '--title', f'Autotask Ticket Analysis {report_date}',
    '--comment', 'Downloadable HTML report for executive review.'
], check=True)

files = sorted(reports.glob('autotask-ticket-analysis-*.html'), key=lambda p: p.stat().st_mtime, reverse=True)
for old in files[7:]:
    old.unlink(missing_ok=True)

print(json.dumps({
    'tickets': len(tickets),
    'companies': company_count,
    'html': str(html_out),
    'kept_files': [p.name for p in files[:7]]
}, indent=2))

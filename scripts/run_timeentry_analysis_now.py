#!/usr/bin/env python3
import json, pathlib, subprocess, re, html
from collections import Counter, defaultdict
from datetime import datetime, timezone

base = pathlib.Path('/root/.openclaw/workspace/tmp/timeentry-live-run')
base.mkdir(parents=True, exist_ok=True)
reports = pathlib.Path('/root/.openclaw/workspace/reports/timeentry')
reports.mkdir(parents=True, exist_ok=True)
now = datetime.now(timezone.utc)
report_date = now.strftime('%Y-%m-%d')
generated_at = now.strftime('%Y-%m-%d %H:%M UTC')

cp = subprocess.run([
    'curl','-sS','-X','POST',
    'https://n8n.grayprotocol.org/webhook/912b740e-fb70-4cad-bcf6-04306b7d7592',
    '-H','Content-Type: application/json',
    '--data','{"code":"TimeEntry24h"}'
], capture_output=True, text=True, check=True)
raw = cp.stdout.strip()
(base / 'webhook-response.json').write_text(raw)
obj = json.loads(raw)
if isinstance(obj, dict) and isinstance(obj.get('data'), list):
    entries = obj['data']
elif isinstance(obj, list):
    entries = obj
elif isinstance(obj, dict):
    entries = [obj]
else:
    entries = []

maintenance_rx = re.compile(r'maintenance|patch|server maintenance|monthly maintenance|3rd thursday', re.I)
automation_rx = re.compile(r'automatically|automated|routine|repeat|same pattern|closed in accordance|template|policy', re.I)
weak_note_rx = re.compile(r'^(checked|worked on issue|fixed issue|see notes|resolved|completed|investigated)\b', re.I)
escalation_rx = re.compile(r'escalat|vendor|waiting on|hand off|handoff|sent to', re.I)

def clean_note(note: str) -> str:
    note = re.sub(r'\s+', ' ', note or '').strip()
    return note[:180] + ('…' if len(note) > 180 else '')

def bulletize(items):
    return '\n'.join(items)

def top_lines(counter, hours_counter=None, limit=3):
    out=[]
    for rid, count in counter.most_common(limit):
        if hours_counter:
            out.append(f'Resource {rid}: {count} entries / {hours_counter[rid]:.2f}h')
        else:
            out.append(f'Resource {rid}: {count}')
    return out or ['No concentration signal yet.']

resource_counts = Counter()
resource_hours = Counter()
maintenance_count = 0
fragment_count = 0
training_findings=[]
automation_findings=[]
waste_findings=[]
doc_findings=[]
appendix=[]
resource_entry_notes=defaultdict(list)

for e in entries:
    rid = str(e.get('resourceID','Unknown'))
    resource_counts[rid] += 1
    hours = float(e.get('hoursWorked') or 0)
    resource_hours[rid] += hours
    note = str(e.get('summaryNotes') or '').strip()
    excerpt = clean_note(note)
    ticket = e.get('ticketID')
    entry_id = e.get('id')
    if maintenance_rx.search(note):
        maintenance_count += 1
    if hours <= 0.25:
        fragment_count += 1
    resource_entry_notes[rid].append({'hours': hours, 'note': note, 'excerpt': excerpt, 'ticket': ticket, 'entry': entry_id})
    appendix.append(f'Entry {entry_id} / Res {rid} / Ticket {ticket} / {hours:.2f}h / {excerpt}')

    if len(note) < 100 or weak_note_rx.search(note):
        training_findings.append((rid, f'Resource {rid} needs tighter note quality and clearer action/outcome detail.', excerpt))
        doc_findings.append((rid, f'Resource {rid} is leaving notes that are too thin to reuse as runbook evidence.', excerpt))
    if automation_rx.search(note):
        automation_findings.append((rid, f'Resource {rid} is spending time on repeatable or policy-shaped work that should be standardized or automated.', excerpt))
    if hours <= 0.25:
        waste_findings.append((rid, f'Resource {rid} is showing fragmented low-duration entries that suggest interrupt-driven work or inefficient task slicing.', excerpt))
    if escalation_rx.search(note):
        doc_findings.append((rid, f'Resource {rid} shows escalation/vendor-dependency patterns that may indicate documentation or triage gaps.', excerpt))

# If signals are sparse, synthesize from dominant resources
for rid, notes in resource_entry_notes.items():
    if len(notes) >= 5 and len(training_findings) < 3:
        worst = sorted(notes, key=lambda n: (len(n['note']), n['hours']))[0]
        training_findings.append((rid, f'Resource {rid} has enough entry volume to justify coaching review of note quality and consistency.', worst['excerpt']))
    if len([n for n in notes if n['hours'] <= 0.25]) >= 5 and len(waste_findings) < 3:
        sample = [n for n in notes if n['hours'] <= 0.25][0]
        waste_findings.append((rid, f'Resource {rid} has repeated quarter-hour fragments that may hide avoidable interruption overhead.', sample['excerpt']))


def uniq_triplets(items):
    out=[]; seen=set()
    for rid, finding, excerpt in items:
        key=(finding, excerpt)
        if key not in seen:
            seen.add(key)
            out.append((rid, finding, excerpt))
    return out

training_findings = uniq_triplets(training_findings)[:3] or [('—','No dominant coaching signal yet from the current batch.','No excerpt needed.')]
automation_findings = uniq_triplets(automation_findings)[:3] or [('—','No dominant automation signal yet from the current batch.','No excerpt needed.')]
waste_findings = uniq_triplets(waste_findings)[:3] or [('—','No dominant time-waste pattern yet from the current batch.','No excerpt needed.')]
doc_findings = uniq_triplets(doc_findings)[:3] or [('—','No dominant documentation/runbook gap yet from the current batch.','No excerpt needed.')]
resource_lines = top_lines(resource_counts, resource_hours, 3)
manager = [training_findings[0][1], automation_findings[0][1], waste_findings[0][1]]

evidence_excerpt = training_findings[0][2] if training_findings else 'No sample note excerpt.'
executive_summary = (
    f'Analyzed {len(entries)} time entries across {len(resource_counts)} resource IDs with primary focus on training, automation, and wasted effort. '
    f'Maintenance was isolated at {maintenance_count} entry(s). The ugliest signals are repetitive quarter-hour fragments, thin summary notes, and policy-shaped work that should not keep stealing technician attention by hand.'
)

ctx_exec = {
    'window_label': 'Webhook 24h batch',
    'entry_count': str(len(entries)),
    'resource_count': str(len(resource_counts)),
    'executive_summary': executive_summary,
    'training_signal': training_findings[0][1],
    'automation_signal': automation_findings[0][1],
    'waste_signal': waste_findings[0][1],
    'hygiene_signal': doc_findings[0][1],
    'maintenance_metric': f'{maintenance_count} maintenance entry(s)',
    'evidence_excerpt': evidence_excerpt,
    'manager_1': manager[0],
    'manager_2': manager[1],
    'manager_3': manager[2]
}
ctx_detail = {
    'generated_at': generated_at,
    'training_1': training_findings[0][1], 'training_ex_1': training_findings[0][2],
    'training_2': training_findings[1][1] if len(training_findings) > 1 else '—', 'training_ex_2': training_findings[1][2] if len(training_findings) > 1 else '—',
    'training_3': training_findings[2][1] if len(training_findings) > 2 else '—', 'training_ex_3': training_findings[2][2] if len(training_findings) > 2 else '—',
    'automation_1': automation_findings[0][1], 'automation_ex_1': automation_findings[0][2],
    'automation_2': automation_findings[1][1] if len(automation_findings) > 1 else '—', 'automation_ex_2': automation_findings[1][2] if len(automation_findings) > 1 else '—',
    'automation_3': automation_findings[2][1] if len(automation_findings) > 2 else '—', 'automation_ex_3': automation_findings[2][2] if len(automation_findings) > 2 else '—',
    'waste_1': waste_findings[0][1], 'waste_ex_1': waste_findings[0][2],
    'waste_2': waste_findings[1][1] if len(waste_findings) > 1 else '—', 'waste_ex_2': waste_findings[1][2] if len(waste_findings) > 1 else '—',
    'waste_3': waste_findings[2][1] if len(waste_findings) > 2 else '—', 'waste_ex_3': waste_findings[2][2] if len(waste_findings) > 2 else '—',
    'doc_1': doc_findings[0][1], 'doc_ex_1': doc_findings[0][2],
    'doc_2': doc_findings[1][1] if len(doc_findings) > 1 else '—', 'doc_ex_2': doc_findings[1][2] if len(doc_findings) > 1 else '—',
    'doc_3': doc_findings[2][1] if len(doc_findings) > 2 else '—', 'doc_ex_3': doc_findings[2][2] if len(doc_findings) > 2 else '—',
    'resource_1': resource_lines[0],
    'resource_2': resource_lines[1] if len(resource_lines) > 1 else '—',
    'resource_3': resource_lines[2] if len(resource_lines) > 2 else '—',
    'appendix_1': appendix[0] if appendix else 'No sample entries',
    'appendix_2': appendix[1] if len(appendix) > 1 else '—',
    'appendix_3': appendix[2] if len(appendix) > 2 else '—'
}

html_blocks = {
    'training': ''.join([f'<div class="finding"><h3>{html.escape(f)}</h3><p class="excerpt">{html.escape(ex)}</p></div>' for _, f, ex in training_findings]),
    'automation': ''.join([f'<div class="finding"><h3>{html.escape(f)}</h3><p class="excerpt">{html.escape(ex)}</p></div>' for _, f, ex in automation_findings]),
    'waste': ''.join([f'<div class="finding"><h3>{html.escape(f)}</h3><p class="excerpt">{html.escape(ex)}</p></div>' for _, f, ex in waste_findings]),
    'docs': ''.join([f'<div class="finding"><h3>{html.escape(f)}</h3><p class="excerpt">{html.escape(ex)}</p></div>' for _, f, ex in doc_findings]),
    'resources': ''.join([f'<li>{html.escape(line)}</li>' for line in resource_lines]),
    'appendix': ''.join([f'<li>{html.escape(line)}</li>' for line in appendix[:8]])
}

html_report = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Time Entry Analysis {report_date}</title>
<style>
:root{{--bg:#0f1117;--panel:#171a23;--soft:#1d2230;--text:#eef2ff;--muted:#aeb7cf;--accent:#d66bff;--accent2:#ff8fcf;--line:rgba(255,255,255,.08);}}
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,sans-serif;background:radial-gradient(circle at top right, rgba(214,107,255,.15), transparent 24%), linear-gradient(180deg,#0c0f16,#101522 60%,#0f121a);color:var(--text)}}
.wrap{{max-width:1180px;margin:0 auto;padding:32px 24px 56px}} .hero{{background:linear-gradient(135deg, rgba(214,107,255,.14), rgba(255,143,207,.10));border:1px solid var(--line);border-radius:26px;padding:28px;box-shadow:0 24px 60px rgba(0,0,0,.25)}}
.eyebrow{{color:var(--accent2);font-size:12px;letter-spacing:.16em;text-transform:uppercase}} h1{{margin:8px 0 10px;font-size:34px;line-height:1.08}} .sub{{color:var(--muted);max-width:900px}}
.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px}} .metric,.card{{background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:18px}} .metric .label{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}} .metric .value{{font-size:28px;font-weight:700;margin-top:8px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}} h2{{margin:0 0 12px;font-size:18px}} h3{{margin:0 0 8px;font-size:15px;line-height:1.35}} .finding{{padding:14px 0;border-top:1px solid var(--line)}} .finding:first-child{{border-top:0;padding-top:0}} .excerpt{{margin:0;color:#ffd8ec;background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:14px;padding:12px;font-size:13px;line-height:1.5}} ul{{margin:0;padding-left:20px}} li{{margin:8px 0}} .footer{{margin-top:18px;color:var(--muted);font-size:13px}}
@media (max-width: 900px){{.metrics,.grid{{grid-template-columns:1fr}}}}
</style></head>
<body><div class="wrap">
<section class="hero"><div class="eyebrow">Manager Review</div><h1>Time Entry Analysis — {report_date}</h1><div class="sub">{html.escape(executive_summary)}</div>
<div class="metrics"><div class="metric"><div class="label">Window</div><div class="value">24h</div></div><div class="metric"><div class="label">Entries</div><div class="value">{len(entries)}</div></div><div class="metric"><div class="label">Resources</div><div class="value">{len(resource_counts)}</div></div><div class="metric"><div class="label">Maintenance</div><div class="value">{maintenance_count}</div></div></div></section>
<section class="grid">
<div class="card"><h2>Training Needs</h2>{html_blocks['training']}</div>
<div class="card"><h2>Automation Opportunities</h2>{html_blocks['automation']}</div>
<div class="card"><h2>Time Waste / Inefficiency</h2>{html_blocks['waste']}</div>
<div class="card"><h2>Hygiene / Documentation Gaps</h2>{html_blocks['docs']}</div>
<div class="card"><h2>Resource Observations</h2><ul>{html_blocks['resources']}</ul></div>
<div class="card"><h2>Sample Appendix</h2><ul>{html_blocks['appendix']}</ul></div>
</section>
<div class="footer">Generated: {generated_at} • Resource IDs only • 7-day local retention</div>
</div></body></html>'''

(base / 'ctx_exec.json').write_text(json.dumps(ctx_exec, indent=2))
(base / 'ctx_detail.json').write_text(json.dumps(ctx_detail, indent=2))
html_out = reports / f'timeentry-analysis-{report_date}.html'
html_out.write_text(html_report)

script_render='/root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/render_blockkit.py'
script_prepare='/root/.openclaw/workspace/scripts/prepare_slack_blockkit_payload.py'
script_adapt='/root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/adapt_to_openclaw_reply_blocks.py'
script_send='/root/.openclaw/workspace/skills/slack-blockkit-notify/scripts/send_openclaw_slack_blocks.mjs'
for name, template, ctx_file, text in [
    ('exec','/root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/timeentry_executive.blockkit.json', base / 'ctx_exec.json', 'Time entry analysis executive summary'),
    ('detail','/root/.openclaw/workspace/skills/slack-blockkit-notify/assets/templates/slack/timeentry_detail.blockkit.json', base / 'ctx_detail.json', 'Time entry analysis detailed breakdown')
]:
    rendered = base / f'{name}.rendered.json'
    payload = base / f'{name}.payload.json'
    adapted = base / f'{name}.openclaw.json'
    subprocess.run(['python3', script_render, '--template', template, '--context', str(ctx_file), '--out', str(rendered)], check=True)
    subprocess.run(['python3', script_prepare, '--channel', 'C0AQWG1UWUC', '--blocks', str(rendered), '--text', text, '--out', str(payload)], check=True)
    subprocess.run(['python3', script_adapt, '--payload', str(payload), '--out', str(adapted)], check=True)
    subprocess.run(['node', script_send, '--payload', str(adapted)], check=True)
subprocess.run(['node','/root/.openclaw/workspace/scripts/upload_slack_file.js','--channel','C0AQWG1UWUC','--file',str(html_out),'--title',f'Time Entry Analysis {report_date}','--comment','Downloadable HTML report for manager review.'], check=True)
files = sorted(reports.glob('timeentry-analysis-*.html'), key=lambda p: p.stat().st_mtime, reverse=True)
for old in files[7:]:
    old.unlink(missing_ok=True)
print(json.dumps({'entries': len(entries), 'resources': len(resource_counts), 'html': str(html_out), 'kept_files': [p.name for p in files[:7]]}, indent=2))

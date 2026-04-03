import json
import os
import subprocess

CUSTOM_LABELS = {
    'to_respond': '1: To Respond',
    'fyi': '2: FYI',
    'comment': '3: Comment',
    'notifications': '4: Notifications',
    'meeting': '5: Meeting Update',
    'awaiting': '6: Awaiting Reply',
    'actioned': '7: Actioned',
    'finance': '8: Finance',
    'family': '9: Family / School',
    'health': '10: Health / Medical',
    'home': '11: Home / Utilities',
    'security': '12: Security / Logins',
    'taxes': '13: Taxes / Legal',
    'travel': '14: Travel / Leisure',
    'subs': '15: Subscriptions / Digital Services',
    'promo': '16: Promotions / Noise',
}


def classify(frm, subject):
    f = (frm or '').lower()
    s = (subject or '').lower()
    text = f + ' ' + s

    if any(x in f for x in ['@gmail.com>', '@layer3technology.com>', '@lodiusd.net>']):
        if any(x in s for x in ['fwd:', 're:', 'cell-phone use', 'public folders', 'exchange 365 issue', 'photos from yesterday', 'top secret', 'collaring']):
            if any(x in s for x in ['school', 'ethan', 'vra', 'uop']):
                return CUSTOM_LABELS['family']
            return CUSTOM_LABELS['to_respond']

    if any(x in text for x in ['authentication code', 'login attempt', 'verification code', '2fa', 'security alert', 'sign-in', 'sign in']):
        return CUSTOM_LABELS['security']
    if any(x in text for x in ['dmv', 'registration renewal', 'utilities', 'insurance bill', 'id cards', 'csaa', 'auto insurance']):
        return CUSTOM_LABELS['home']
    if any(x in text for x in ['turbotax', 'w-2', 'tax', 'trinet', 'payment was received', 'receipt', 'order confirmation', 'invoice', 'federal return accepted']):
        return CUSTOM_LABELS['finance']
    if any(x in text for x in ['medical', 'health', 'pre auth', 'pre-auth', 'intolerance test', 'adapthealth', 'doctor', 'dr.']):
        return CUSTOM_LABELS['health']
    if any(x in text for x in ['school', 'delta college', 'lodiusd', 'powerschool', 'ethan', 'eli stacy', 'vra', 'uop summer program', 'college early start']):
        return CUSTOM_LABELS['family']
    if any(x in text for x in ['patreon', 'podcast', 'sly flourish', 'kindle', 'unity', 'netspot', 'serial numbers', 'asset store', 'bookstore', 'power prompts', 'wires-x', 'hamstudy', 'rt systems']):
        return CUSTOM_LABELS['subs']
    if any(x in text for x in ['etsy', 'download your etsy purchase', 'order has shipped', 'new order', 'welcome to team hunt', 'shipped', 'purchase', 'hunt by onxmaps', 'powerwerx']):
        return CUSTOM_LABELS['subs']
    if any(x in text for x in ['pitboss', 'pit boss', 'promotions', 'marketing@', 'dansons.com']):
        return CUSTOM_LABELS['promo']
    if any(x in text for x in ['update:', 'notification', 'license recovery', 'account registration completed', 'signed copy']):
        return CUSTOM_LABELS['notifications']
    if any(x in s for x in ['meeting', 'calendar invite', 'invite update']):
        return CUSTOM_LABELS['meeting']
    if any(x in text for x in ['fwd:', 're:']):
        return CUSTOM_LABELS['to_respond']
    return CUSTOM_LABELS['fyi']


def main():
    env = os.environ.copy()
    query = 'in:inbox -label:"1: To Respond" -label:"2: FYI" -label:"3: Comment" -label:"4: Notifications" -label:"5: Meeting Update" -label:"6: Awaiting Reply" -label:"7: Actioned" -label:"8: Finance" -label:"9: Family / School" -label:"10: Health / Medical" -label:"11: Home / Utilities" -label:"12: Security / Logins" -label:"13: Taxes / Legal" -label:"14: Travel / Leisure" -label:"15: Subscriptions / Digital Services" -label:"16: Promotions / Noise"'
    proc = subprocess.run(['gog', 'gmail', 'search', query, '--all', '--json'], capture_output=True, text=True, env=env)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout)
    data = json.loads(proc.stdout)
    threads = data.get('threads', [])
    applied = 0
    for t in threads:
        label = classify(t.get('from', ''), t.get('subject', ''))
        mod = subprocess.run(['gog', 'gmail', 'threads', 'modify', t['id'], '--add', label, '--no-input'], capture_output=True, text=True, env=env)
        if mod.returncode == 0:
            applied += 1
    print(f'labeled {applied} of {len(threads)} unlabeled inbox threads')


if __name__ == '__main__':
    main()

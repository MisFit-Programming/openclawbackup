Run a read-only nightly security review of the workspace/repo.

Checks:
- `git status --short`
- `git ls-files | grep -Ei '(^|/)(\.env|\.env\.|.*secret.*|.*token.*|.*credential.*|.*key.*\.pem$|.*private.*key.*)' || true`
- review `.gitignore` for `.env` / secret coverage
- `find /root/.openclaw/workspace -maxdepth 4 -type f | grep -Ei '\.(env|pem|key|p12|pfx)$' || true`
- `du -sh /root/.openclaw/workspace`
- `git count-objects -vH`

If anything looks risky (tracked secrets, suspicious files, large unexpected growth), summarize the issue and safest next step in a compact Block Kit-style health/update summary for Slack channel C0AQARFMWMV. If nothing meaningful is wrong, return NO_REPLY.

Never print or send raw secrets. Redact suspicious filenames if necessary.
Return only a one-line success/failure summary.
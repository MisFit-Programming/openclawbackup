Run a read-only repo size / leak monitor.

Checks:
- `du -sh /root/.openclaw/workspace`
- `git count-objects -vH`
- largest files under workspace (`find ... -printf '%s %p' | sort -nr | head` or equivalent)
- unexpected recent growth in tmp/runtime/output areas

If size or file growth looks suspicious or leak-like, send a concise Slack alert to C0AQARFMWMV with what grew, where, and the safest next step. If normal, return NO_REPLY.
Do not delete anything.
Return only a one-line success/failure summary.
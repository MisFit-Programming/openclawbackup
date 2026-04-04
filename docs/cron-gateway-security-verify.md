Run a read-only weekly gateway/OpenClaw security verification.

Checks:
- `openclaw security audit --deep`
- `openclaw update status`
- `openclaw status --deep`
- confirm loopback binding / exposure posture from output
- confirm auth/security posture from audit output
- note any listeners that look broader than expected

If issues are found, send a concise executive-clean Slack health report to channel C0AQARFMWMV with what changed, risk level, and safest next command. If healthy, send a compact success card no more than once per run.
Do not make state changes.
Return only a one-line success/failure summary.
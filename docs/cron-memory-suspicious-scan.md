Run a read-only monthly scan of memory files for suspicious patterns or accidental sensitive retention.

Scope:
- `/root/.openclaw/workspace/memory/*.md`
- `/root/.openclaw/workspace/MEMORY.md` if present

Checks:
- obvious API key/token/password/private key patterns
- copied credentials or secrets
- excessive raw logs
- financial/account numbers that should not sit in shared memory files
- notes that belong in DM-only contexts rather than shared/group-safe memory

If suspicious content is found, send a concise alert to Slack channel C0AQARFMWMV with the file path, issue type, and safest remediation suggestion. Do not include the raw secret.
If nothing meaningful is found, return NO_REPLY.
Return only a one-line success/failure summary.
# Repository rules for automated backup

## Target repo

- Remote: `origin`
- Branch: `main`
- Repo: `git@github.com:MisFit-Programming/openclawbackup.git`

## Goal

Preserve Dobbie's continuity files and workspace evolution in a private GitHub repository without committing obvious junk or secrets.

## Include by default

- `memory/`
- `skills/`
- `scripts/`
- `templates/`
- useful workspace docs and configuration
- packaged `.skill` files when intentionally created

## Exclude by default

Rely on `.gitignore`, especially for:
- `.env*`
- `*client_secret*.json`
- keys/certs
- runtime/transient state
- editor/temp files
- dependency caches

## Commit message rules

Prefer descriptive messages that summarize what changed.
Good examples:
- `Memory updates + new maintenance skill + Slack Block Kit templates`
- `Automations: convert cron jobs to Block Kit sender path`
- `Workspace backup setup + gitignore hardening`

Avoid:
- `daily backup`
- `auto commit`
- `updates`

## Failure handling

- If there are no changes, exit quietly.
- If push fails, retry once.
- If push still fails, stop and report failure.

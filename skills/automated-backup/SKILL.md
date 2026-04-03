---
name: automated-backup
description: Commit and push workspace changes to the configured private Git repository on a schedule using descriptive commit messages and safe default exclusions. Use when setting up or running recurring backups for Dobbie’s workspace, preserving memory, skills, scripts, templates, and other continuity files without pushing obvious junk or secrets.
---

# automated-backup

Back up Dobbie’s workspace to the configured private Git repository in a safe, descriptive, repeatable way.

## Workflow

1. Work in the workspace repository.
   - Repository root: `/root/.openclaw/workspace`
   - Read `references/repo-rules.md` for the target remote/branch and backup rules.

2. Check whether anything changed.
   - Run `git status --porcelain`.
   - If there are no changes, exit quietly.

3. Respect `.gitignore`.
   - Do not force-add ignored files.
   - Do not intentionally add obvious secret-bearing files or transient runtime clutter.

4. Stage safely.
   - Use `git add -A`.
   - Trust `.gitignore` for excluded patterns.

5. Generate a descriptive commit message.
   - Use the staged diff summary to describe what changed.
   - Make it readable at a glance.
   - Never use lazy messages like `daily backup` or `auto commit`.

6. Commit and push.
   - Commit only if there is staged content.
   - Push to `origin main`.
   - If push fails, retry once.
   - If it still fails, report the failure.

7. Report briefly.
   - Include whether changes existed, commit hash if created, and push success/failure.

## Practical rules

- Preserve continuity files and workflow assets.
- Keep secrets out of Git.
- Prefer one good descriptive commit over generic noise.
- Skip empty commits.
- Treat backup as preservation, not random cleanup.

## Read this reference when doing the work

- `references/repo-rules.md`

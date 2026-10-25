# Relocation job tracker

Android jobs that offer relocation and visa sponsorship, found automatically by Claude, with a small website to track each one.

**Website: https://khudoyshukur.github.io/relocation/**

## How it works

- **`data/jobs.json`**: jobs found so far. Every 8 hours `.github/workflows/find-jobs.yml` runs Claude Code (on a Claude subscription). Claude follows `.github/prompts/find-jobs.md` and `profile.md`, searches the web, confirms each posting is still open, and writes `data/new_jobs.json`. Then `scripts/merge_jobs.py` adds the new jobs and marks closed ones.
- **`data/tracking.json`**: your statuses, notes and archive flags, **encrypted** (AES-GCM), so they stay unreadable even if the repo is ever made public. Only the website writes this file.
- **`site/index.html`**: the website, published to GitHub Pages by `.github/workflows/deploy-site.yml`. At deploy time `scripts/build-config.mjs` encrypts a GitHub token and the notes key with the site username and password. Logging in decrypts them, so a wrong password unlocks nothing.

## Secrets (Settings → Secrets and variables → Actions)

| Secret | What it is |
|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | From `claude setup-token`; runs the job search on a Claude subscription |
| `SITE_USERNAME`, `SITE_PASSWORD` | Website login |
| `SITE_GH_TOKEN` | [Fine-grained token](https://github.com/settings/personal-access-tokens/new): only this repo, **Contents: Read and write**. Lets the website save notes |
| `SITE_DATA_KEY` | Random key that encrypts the notes. Don't change it, or existing notes can't be read |

After changing any `SITE_*` secret, re-run Actions → "Deploy site" → Run workflow.

Run a search right away from Actions → "Find relocation jobs" → Run workflow.

## Costs

Each search run is capped at 20 minutes, so at most ~1,800 Actions minutes a month (free plan: 2,000 for private repos; Pro: 3,000). In practice a run takes about 2 minutes. Searches also count toward your Claude subscription usage.

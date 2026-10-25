# Relocation job tracker

Android jobs that offer relocation and visa sponsorship, found automatically by Claude, with a small website to track each one.

**Website: https://khudoyshukur.github.io/relocation/**

## How it works

- **`data/companies.json`**: every company being watched, with its careers page and, where possible, its job board (Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Recruitee, Personio). Edit it to add or remove companies. Claude also adds companies it discovers.
- **Every 8 hours** `.github/workflows/find-jobs.yml`:
  1. `scripts/scan_boards.py` reads every job board in `data/companies.json` and saves the Android-looking postings to `data/board_scan.json`. This is free and needs no AI.
  2. `scripts/pick_companies.py` picks the next 25 companies without a scannable board, so all of them are covered in rotation.
  3. Claude Code (on a Claude subscription) follows `.github/prompts/find-jobs.md` and `profile.md`. It reviews the scanned postings, checks the picked companies, searches the wider web, confirms each posting is open, and writes `data/new_jobs.json`.
  4. `scripts/merge_jobs.py` adds new jobs and companies to `data/jobs.json` and `data/companies.json`, and marks closed jobs.
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

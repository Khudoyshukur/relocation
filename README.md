# Relocation job tracker

Android jobs that offer relocation and visa sponsorship, found automatically by Claude, with a small website to track each one.

**Website: https://khudoyshukur.github.io/relocation/**

## How it works

- **`data/jobs.json`**: jobs found so far. Every 8 hours `.github/workflows/find-jobs.yml` runs Claude Code (on a Claude subscription). Claude follows `.github/prompts/find-jobs.md` and `profile.md`, searches the web, confirms each posting is still open, and writes `data/new_jobs.json`. Then `scripts/merge_jobs.py` adds the new jobs and marks closed ones.
- **`data/tracking.json`**: your statuses, notes and archive flags. Only the website writes this file.
- **`site/index.html`**: the website, published to GitHub Pages by `.github/workflows/deploy-site.yml`. Only this page is published. It loads the data from this private repo through the GitHub API with a fine-grained token you paste in once (kept in your browser only).

## Setup

1. Repo secret `CLAUDE_CODE_OAUTH_TOKEN`: run `claude setup-token` locally and paste the result into Settings → Secrets and variables → Actions.
2. Website token: create a [fine-grained token](https://github.com/settings/personal-access-tokens/new) with access to only this repo and **Contents: Read and write**, then paste it into the site.

Run a search right away from the Actions tab → "Find relocation jobs" → Run workflow.

## Costs

Each search run is capped at 20 minutes, so at most ~1,800 Actions minutes a month (free plan: 2,000 for private repos; Pro: 3,000). Searches also count toward your Claude subscription usage.

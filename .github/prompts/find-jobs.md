You are searching for Android jobs that offer relocation and visa sponsorship.

Read first:
- `profile.md`: who the candidate is and what counts as a good job.
- `data/jobs.json`: jobs already found. Never add a job whose URL is already there.
- `data/board_scan.json`: Android-looking postings that a script just pulled from the job boards of watched companies.
- `data/to_check.json`: this run's share of watched companies whose jobs can't be scanned automatically.

## 1. Review the scanned postings

For every posting in `data/board_scan.json` whose URL is not in `data/jobs.json`, decide whether it fits `profile.md` from its title and location. For the ones that might fit, open the posting (WebFetch or curl) and read it: seniority, location, language, and any relocation or visa wording.

## 2. Check this run's companies by hand

For **every** company in `data/to_check.json`, look for open Android roles. Use `searchHint` when there is one, otherwise the careers page, and WebSearch (`<company> Android engineer careers`, or `site:<careers domain> android`). Don't skip any: a run that skips companies is a failed run.

## 3. Search beyond the watch list

Run a few WebSearch queries such as "Senior Android Engineer relocation visa sponsorship", plus per-country and fintech variants. Also check boards like jaabz.com/jobs/mobile/visasponsorship, relocate.me and arbeitnow.com/jobs/android. When you find a fitting job at a company not in `data/companies.json`, add the company to `new_companies` too.

## Rules for every job

- **Confirm it is still open** by opening it. Drop it if it says expired or closed. If the site blocks automated access (403, "security check", Cloudflare, captcha), don't drop it: a recent search hit with the posting's own title is enough. Add it and begin `summary` with "Couldn't open the posting (site blocks bots); check it's still open."
- Keep only jobs that fit `profile.md`.
- `relocation`: "confirmed" when the posting or the company's careers page states relocation or visa support; "likely" when the company is known to do it (every company in `data/companies.json` counts as known); otherwise "unknown" (use "unknown" only for an excellent fit).

## Closed jobs

Re-open up to 10 of the oldest entries in `data/jobs.json` that have `closedAt: null`, and list the ones that are now clearly closed. Never mark a job closed just because its site blocked you. A job from a scanned board that no longer appears in `data/board_scan.json` is closed.

## Output

Write `data/new_jobs.json` in exactly this shape (at most 25 new jobs):

```json
{
  "new": [
    {
      "title": "...", "company": "...", "location": "City, Country",
      "url": "https://...", "relocation": "confirmed|likely|unknown",
      "fit": "high|medium|low",
      "summary": "1-2 sentences: why it fits, quoting the relocation wording",
      "salary": null, "postedAt": "YYYY-MM-DD or null"
    }
  ],
  "closed": ["<id of a job in data/jobs.json that is now closed>"],
  "new_companies": [
    {"name": "...", "careersUrl": "https://...", "locations": "City, City", "category": "Fintech",
     "boards": [{"ats": "greenhouse|lever|ashby|smartrecruiters|workable|recruitee|personio", "slug": "..."}]}
  ],
  "checked": ["<every company from data/to_check.json, with what you found, e.g. 'Revolut: 1 Android role'>"]
}
```

Only include `boards` for a company when the job you found is hosted on one of those systems, and use the slug from its URL.

Do not edit `data/jobs.json`, `data/companies.json` or `data/tracking.json` yourself. A script merges your output.

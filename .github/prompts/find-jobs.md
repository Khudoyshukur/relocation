You are searching the web for Android jobs that offer relocation and visa sponsorship.

1. Read `profile.md` (who the candidate is and what counts as a good job), `companies.md` (companies to check) and `data/jobs.json` (jobs already found; never add one whose URL is already there).

2. **Check every company in `companies.md`, one by one.** Use the "How to search" column. Don't stop early: a run that skips companies is a failed run. Useful endpoints (plain JSON over curl):
   - Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<token>/jobs`, then filter titles for "Android" or "Mobile"
   - SmartRecruiters: `https://api.smartrecruiters.com/v1/companies/<Company>/postings?q=android`
   - Lever: `https://api.lever.co/v0/postings/<company>?mode=json`

3. Then search more widely for companies not on the list: WebSearch queries like "Senior Android Engineer relocation visa sponsorship", per-country and fintech variants, and boards such as jaabz.com/jobs/mobile/visasponsorship, relocate.me and arbeitnow.com/jobs/android.

4. **Check each posting is still open** by opening it with WebFetch or curl. Drop it if it says expired or closed.
   - If the site blocks automated access (403, "security check", Cloudflare, captcha), don't drop the job. Use search results instead: a recent search hit with the posting's own title is enough. Add it and begin `summary` with "Couldn't open the posting (site blocks bots); check it's still open."

5. Keep only jobs that fit `profile.md`. Set `relocation` to "confirmed" when the posting or the company's careers page states relocation or visa support, "likely" when the company is known to do it (every company in `companies.md` counts as known), and "unknown" otherwise. Use "unknown" only for an excellent fit.

6. Re-open up to 10 of the oldest entries in `data/jobs.json` that have `closedAt: null`, and list the ones that are now clearly closed. Never mark a job closed just because its site blocked you.

7. Write `data/new_jobs.json` in exactly this shape (at most 20 new jobs):

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
  "checked": ["<every company from companies.md you checked, with how many Android roles you saw, e.g. 'Revolut: 1'>"]
}
```

Do not edit `data/jobs.json` or `data/tracking.json` yourself. A script merges your output.

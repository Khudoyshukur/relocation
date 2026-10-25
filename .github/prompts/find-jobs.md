You are searching the web for Android jobs that offer relocation and visa sponsorship.

1. Read `profile.md` (who the candidate is and what counts as a good job) and `data/jobs.json` (jobs already found; never add one whose URL is already there).
2. Search for new postings:
   - WebSearch queries such as "Senior Android Engineer relocation visa sponsorship", per-country variants, and fintech-focused variants.
   - Company job boards that answer plain JSON over curl:
     - Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<token>/jobs` (e.g. monzo, adyen, n26, wise, wolt, getyourguide, hellofresh, doctolib)
     - SmartRecruiters: `https://api.smartrecruiters.com/v1/companies/<Company>/postings?q=android` (e.g. DeliveryHero)
     - Lever: `https://api.lever.co/v0/postings/<company>?mode=json`
   - Boards: jaabz.com/jobs/mobile/visasponsorship, relocate.me, arbeitnow.com/jobs/android, adjoe.io/careers.
   - Companies known to relocate Android engineers: adjoe, Revolut, Scalable Capital, Delivery Hero / HungerStation / Talabat / Glovo, Agoda, Booking.com, Spotify, Bolt, Wolt, Zalando, N26, Wise, Klarna, SumUp, Trade Republic, JetBrains, Exness, Careem, Grab.
3. Open every candidate posting with WebFetch or curl and confirm that it is **still open**. Many listings online are stale, so drop anything that says expired or closed, or that you can't confirm.
4. Keep only jobs that fit `profile.md`. Set `relocation` to "confirmed" when the posting or the company careers page states relocation or visa support, "likely" when the company is known to do it, and "unknown" otherwise (use "unknown" only for an excellent fit).
5. Also re-open up to 10 of the oldest entries in `data/jobs.json` that have `closedAt: null`, and list the ones that are now closed.
6. Write `data/new_jobs.json` in exactly this shape (at most 15 new jobs):

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
  "closed": ["<id of a job in data/jobs.json that is now closed>"]
}
```

Do not edit `data/jobs.json` or `data/tracking.json` yourself. A script merges your output.

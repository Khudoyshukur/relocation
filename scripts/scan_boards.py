"""Scan the job boards listed in data/companies.json for Android roles.

Writes data/board_scan.json: every Android-looking posting per company, so the
website can show live counts and Claude only has to review a short list.
Uses only the standard library. A board that fails is reported, not fatal.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPANIES = ROOT / "data" / "companies.json"
OUT = ROOT / "data" / "board_scan.json"

UA = "Mozilla/5.0 (compatible; relocation-job-tracker/1.0)"
# Android roles, plus generic "Mobile" roles that aren't iOS-only.
ANDROID = re.compile(r"android|kotlin", re.I)
MOBILE = re.compile(r"\bmobile\b", re.I)
IOS_ONLY = re.compile(r"\bios\b|swift", re.I)


def is_android(title: str) -> bool:
    return bool(ANDROID.search(title) or (MOBILE.search(title) and not IOS_ONLY.search(title)))


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def scan_board(ats: str, slug: str) -> list[dict]:
    """All postings on one board as {title, location, url}."""
    if ats == "greenhouse":
        d = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
        return [{"title": j["title"], "location": (j.get("location") or {}).get("name", ""), "url": j["absolute_url"]}
                for j in d.get("jobs", [])]
    if ats in ("lever", "lever-eu"):
        host = "api.eu.lever.co" if ats == "lever-eu" else "api.lever.co"
        d = fetch_json(f"https://{host}/v0/postings/{slug}?mode=json")
        return [{"title": j["text"], "location": (j.get("categories") or {}).get("location", ""), "url": j["hostedUrl"]}
                for j in d]
    if ats == "ashby":
        d = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
        return [{"title": j["title"], "location": j.get("location", ""), "url": j.get("jobUrl", "")}
                for j in d.get("jobs", [])]
    if ats == "smartrecruiters":
        out, offset = [], 0
        while True:
            d = fetch_json(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?q=android&limit=100&offset={offset}")
            for j in d.get("content", []):
                loc = j.get("location") or {}
                out.append({"title": j["name"], "location": ", ".join(x for x in (loc.get("city"), loc.get("country", "").upper()) if x),
                            "url": f"https://jobs.smartrecruiters.com/{slug}/{j['id']}"})
            offset += 100
            if offset >= d.get("totalFound", 0) or offset >= 500:
                return out
    if ats == "workable":
        d = fetch_json(f"https://apply.workable.com/api/v1/widget/accounts/{slug}")
        return [{"title": j["title"], "location": ", ".join(x for x in (j.get("city"), j.get("country")) if x),
                 "url": j.get("url") or j.get("shortlink") or f"https://apply.workable.com/{slug}/"}
                for j in d.get("jobs", [])]
    if ats == "recruitee":
        d = fetch_json(f"https://{slug}.recruitee.com/api/offers/")
        return [{"title": j["title"], "location": j.get("location", ""), "url": j.get("careers_url", "")}
                for j in d.get("offers", [])]
    if ats == "personio":
        xml = fetch_text(f"https://{slug}.jobs.personio.de/xml")
        out = []
        for pos in re.findall(r"<position>(.*?)</position>", xml, re.S):
            title = re.search(r"<name>(.*?)</name>", pos, re.S)
            jid = re.search(r"<id>(\d+)</id>", pos)
            office = re.search(r"<office>(.*?)</office>", pos, re.S)
            if title and jid:
                out.append({"title": title.group(1).strip(), "location": office.group(1).strip() if office else "",
                            "url": f"https://{slug}.jobs.personio.de/job/{jid.group(1)}"})
        return out
    raise ValueError(f"unknown ATS {ats}")


def scan_company(company: dict) -> tuple[str, dict]:
    jobs, errors = [], []
    for b in company.get("boards", []):
        try:
            jobs += [j for j in scan_board(b["ats"], b["slug"]) if is_android(j["title"])]
        except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError, TimeoutError) as err:
            errors.append(f"{b['ats']}:{b['slug']}: {err}")
    seen, unique = set(), []
    for j in jobs:
        if j["url"] not in seen:
            seen.add(j["url"]); unique.append(j)
    return company["name"], {"jobs": unique, "errors": errors}


def main() -> None:
    companies = [c for c in json.loads(COMPANIES.read_text()) if c.get("boards")]
    with ThreadPoolExecutor(16) as ex:
        results = dict(ex.map(scan_company, companies))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.write_text(json.dumps({"scannedAt": now, "companies": results}, indent=1, ensure_ascii=False) + "\n")
    total = sum(len(r["jobs"]) for r in results.values())
    failed = [n for n, r in results.items() if r["errors"]]
    print(f"scanned {len(results)} boards: {total} Android-looking postings; {len(failed)} with errors {failed}")


if __name__ == "__main__":
    main()

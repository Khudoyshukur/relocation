"""Merge Claude's search results (data/new_jobs.json) into data/jobs.json.

Skips jobs whose URL is already known, gives each new job a stable id,
and marks jobs Claude reported as closed. Safe to run when the results
file is missing or malformed: it then leaves jobs.json unchanged.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
JOBS = ROOT / "data" / "jobs.json"
NEW = ROOT / "data" / "new_jobs.json"

FIELDS = ["title", "company", "location", "url", "relocation", "fit", "summary", "salary", "postedAt"]
CHOICES = {"relocation": {"confirmed", "likely", "unknown"}, "fit": {"high", "medium", "low"}}


def normalize_url(url: str) -> str:
    """Drop query strings, fragments and trailing slashes so the same posting matches."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    host = re.sub(r"^[a-z]{2}\.linkedin\.com$", "linkedin.com", host)
    return urlunsplit(("https", host, parts.path.rstrip("/"), "", ""))


def make_id(company: str, title: str, url: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", f"{company}-{title}".lower()).strip("-")[:50]
    return f"{slug}-{hashlib.sha1(normalize_url(url).encode()).hexdigest()[:6]}"


def clean(job: dict) -> dict | None:
    if not isinstance(job, dict):
        return None
    out = {k: job.get(k) for k in FIELDS}
    for key in ("title", "company", "url"):
        if not isinstance(out[key], str) or not out[key].strip():
            return None
    if not out["url"].startswith(("http://", "https://")):
        return None
    for key, allowed in CHOICES.items():
        if out[key] not in allowed:
            out[key] = "unknown" if key == "relocation" else "medium"
    for key in ("location", "summary", "salary", "postedAt"):
        if out[key] is not None and not isinstance(out[key], str):
            out[key] = str(out[key])
    return out


def main() -> int:
    jobs = json.loads(JOBS.read_text())
    if not NEW.exists():
        print("no data/new_jobs.json; nothing to merge")
        return 0
    try:
        result = json.loads(NEW.read_text())
    except json.JSONDecodeError as err:
        print(f"data/new_jobs.json is not valid JSON ({err}); skipping")
        NEW.unlink()
        return 0

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    known = {normalize_url(j["url"]) for j in jobs}

    added = 0
    for raw in result.get("new", []) if isinstance(result, dict) else []:
        job = clean(raw)
        if not job or normalize_url(job["url"]) in known:
            continue
        known.add(normalize_url(job["url"]))
        jobs.append({"id": make_id(job["company"], job["title"], job["url"]), **job,
                     "foundAt": now, "closedAt": None})
        added += 1

    closed_ids = set(result.get("closed", [])) if isinstance(result, dict) else set()
    closed = 0
    for job in jobs:
        if job["id"] in closed_ids and not job.get("closedAt"):
            job["closedAt"] = now
            closed += 1

    checked = result.get("checked", []) if isinstance(result, dict) else []
    print(f"companies checked ({len(checked)}):")
    for line in checked:
        print(f"  {line}")

    JOBS.write_text(json.dumps(jobs, indent=2, ensure_ascii=False) + "\n")
    NEW.unlink()
    print(f"added {added} job(s), marked {closed} closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Pick this run's share of companies whose job boards can't be scanned automatically.

Claude checks these by hand (careers page / web search). Rotating a fixed-size
slice each run covers the whole list every few days without long runs.
Writes data/to_check.json.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PER_RUN = 25
RUN_HOURS = 8

companies = sorted((c for c in json.loads((ROOT / "data" / "companies.json").read_text()) if not c.get("boards")),
                   key=lambda c: c["name"].lower())
slices = max(1, math.ceil(len(companies) / PER_RUN))
index = int(time.time() // (RUN_HOURS * 3600)) % slices
picked = companies[index * PER_RUN:(index + 1) * PER_RUN]

(ROOT / "data" / "to_check.json").write_text(json.dumps(
    [{k: c.get(k) for k in ("name", "careersUrl", "locations", "searchHint")} for c in picked],
    indent=1, ensure_ascii=False) + "\n")
print(f"slice {index + 1}/{slices}: {len(picked)} of {len(companies)} companies without a scannable board")

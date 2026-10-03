import glob
import json
import os
from typing import Any

SRC = "/data/weather/logs/windy"
DST = "tmp/logs/windy"

logs = sorted(glob.glob(os.path.join(SRC, "**", "*.jsonl"), recursive=True))

current: dict[str, Any] | None = None
for src in logs:
    rel = os.path.relpath(src, SRC)
    dst = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    print(f"{src} -> {dst}")
    with open(src, "r") as r, open(dst, "w") as w:
        for row in r:
            rec = json.loads(row)
            if current:
                current.update(rec)
            else:
                current = rec
            w.write(json.dumps(current) + "\n")

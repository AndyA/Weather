import glob
import json
import os
from datetime import datetime, timedelta

SRC = "/data/weather/logs/windy"
DST = "tmp/logs/windy"

logs = sorted(glob.glob(os.path.join(SRC, "**", "*.jsonl"), recursive=True))

for src in logs:
    rel = os.path.relpath(src, SRC)
    dst = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    print(f"{src} -> {dst}")
    with open(src, "r") as r, open(dst, "w") as w:
        rows = [json.loads(row) for row in r]
        if len(rows) == 0:
            continue
        first = datetime.fromisoformat(rows[0]["time"]).replace(
            minute=0,
            second=0,
            microsecond=0,
        )
        pos = 0
        rec = rows[pos]
        for second in range(3600):
            stamp = first + timedelta(seconds=second)
            limit = (stamp + timedelta(seconds=1)).isoformat()
            rec["time"] = stamp.isoformat()
            w.write(json.dumps(rec) + "\n")
            while pos < len(rows) and rows[pos]["time"] < limit:
                rec = rows[pos]
                pos += 1

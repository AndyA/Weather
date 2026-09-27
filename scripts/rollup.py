import glob
import json
import os
from typing import Any

SRC = "/data/weather/logs/windy"
DST = "tmp/windy.jsonl"

logs = sorted(glob.glob(os.path.join(SRC, "**", "*.jsonl"), recursive=True))

current: dict[str, Any] | None = None
with open(DST, "w") as w:
    for log in logs:
        with open(log, "r") as r:
            for row in r:
                rec = json.loads(row)
                if current:
                    current.update(rec)
                else:
                    current = rec
                w.write(json.dumps(current) + "\n")

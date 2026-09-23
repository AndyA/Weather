import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(kw_only=True, frozen=True)
class JsonLogger:
    prefix: str

    def filename(self, ts: datetime) -> str:
        return os.path.join(self.prefix, ts.strftime("%Y/%m/%d/%H.jsonl"))

    def append(self, ts: datetime, payload: dict[str, Any]) -> None:
        path = self.filename(ts)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a") as f:
            json.dump(payload, f)
            f.write("\n")

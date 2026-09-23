from dataclasses import dataclass
from datetime import datetime
from typing import Any

from lib.json_logger import JsonLogger
from lib.tools import obj_diff


@dataclass(kw_only=True)
class DeltaLogger:
    logger: JsonLogger
    verbose: bool = False
    prev_payload: dict[str, Any] | None = None
    prev_filename: str | None = None

    def append(self, ts: datetime, payload: dict[str, Any]) -> None:
        filename = self.logger.filename(ts)
        if filename != self.prev_filename:
            self.prev_payload = None
            self.prev_filename = filename

        delta = obj_diff(self.prev_payload, payload)
        self.prev_payload = payload

        if len(delta):
            obj: dict[str, str | int] = {"time": ts.isoformat(), **delta}
            self.logger.append(ts, obj)
            if self.verbose:
                print(obj)

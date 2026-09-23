import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime

from lib.reading import Reading
from lib.sources import FileSource, SerialSource
from tinyflux import Point, TinyFlux


@dataclass(kw_only=True)
class TinyFluxLogger:
    prefix: str
    handle: TinyFlux | None = None
    current: str | None = None

    def db(self, ts: datetime) -> TinyFlux:
        path = os.path.join(self.prefix, ts.strftime("%Y/%m/%d/%H.csv"))
        if path != self.current:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.handle = TinyFlux(path)
            self.current = path

        assert self.handle is not None
        return self.handle


def obj_diff(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {k: v for k, v in b.items() if a[k] != v}


DRYRUN = True

if DRYRUN:
    source = FileSource(name="ref/weather.log")
    logger = TinyFluxLogger(prefix="tmp/logs")
else:
    source = SerialSource(port="/dev/serial0")
    logger = TinyFluxLogger(prefix="/data/logs/weather")

prev: dict[str, int] | None = None
for line in source.messages():
    now = datetime.now(UTC)
    reading = Reading(line=line)
    point = Point(time=now, measurement="weather", fields=reading.index)
    logger.db(now).insert(point)
    if prev:
        delta = obj_diff(prev, reading.index)
    else:
        delta = reading.index
    prev = reading.index
    if len(delta):
        diff: dict[str, str | int] = {"time": now.isoformat(), **delta}
        print(json.dumps(diff))

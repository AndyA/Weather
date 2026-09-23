import json
import platform
from datetime import UTC, datetime

from lib.json_logger import JsonLogger
from lib.reading import Reading
from lib.sources import FileSource, SerialSource
from lib.tinyflux_logger import TinyFluxLogger
from lib.tools import obj_diff
from tinyflux import Point

DRYRUN = platform.node() != "windy"

if DRYRUN:
    source = FileSource(name="ref/weather.log")
    tf_logger = TinyFluxLogger(prefix="tmp/logs/tinyflux")
    j_logger = JsonLogger(prefix="tmp/logs/json")
else:
    source = SerialSource(port="/dev/serial0")
    tf_logger = TinyFluxLogger(prefix="/data/logs/weather")
    j_logger = JsonLogger(prefix="/data/logs/windy")


prev: dict[str, int] | None = None
prev_log: str | None = None
for line in source.messages():
    now = datetime.now(UTC)

    # TinyFlux
    reading = Reading(line=line)
    point = Point(time=now, measurement="weather", fields=reading.index)
    tf_logger.db(now).insert(point)

    # Json
    log = j_logger.filename(now)
    if prev_log != log:
        prev = None
        prev_log = log

    delta = obj_diff(prev, reading.index)
    prev = reading.index

    if len(delta):
        payload: dict[str, str | int] = {"time": now.isoformat(), **delta}
        print(json.dumps(payload))
        j_logger.append(now, payload)

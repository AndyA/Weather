import json
import platform
from datetime import UTC, datetime

from lib.json_logger import JsonLogger
from lib.reading import Reading
from lib.sources import FileSource, SerialSource
from lib.tools import obj_diff

DRYRUN = platform.node() != "windy"

if DRYRUN:
    source = FileSource(name="ref/weather.log")
    j_logger = JsonLogger(prefix="tmp/logs/json")
else:
    source = SerialSource(port="/dev/serial0")
    j_logger = JsonLogger(prefix="/data/weather/logs/windy")


prev: dict[str, int] | None = None
prev_log: str | None = None
for line in source.messages():
    now = datetime.now(UTC)
    reading = Reading(line=line)

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

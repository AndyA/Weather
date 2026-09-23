import platform
from datetime import UTC, datetime

from lib.delta_logger import DeltaLogger
from lib.json_logger import JsonLogger
from lib.reading import Reading
from lib.sources import FileSource, SerialSource

DRYRUN = platform.node() != "windy"

if DRYRUN:
    source = FileSource(name="ref/weather.log")
    json_logger = JsonLogger(prefix="tmp/logs/json")
else:
    source = SerialSource(port="/dev/serial0")
    json_logger = JsonLogger(prefix="/data/weather/logs/windy")

logger = DeltaLogger(logger=json_logger, verbose=True)

for line in source.messages():
    now = datetime.now(UTC)
    reading = Reading(line=line)
    logger.append(now, reading.index)

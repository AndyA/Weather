import glob

from lib.json_logger import JsonLogger
from lib.tools import obj_diff
from tinyflux import MeasurementQuery, TinyFlux

logger = JsonLogger(prefix="/data/weather/logs/windy")


for log in glob.glob("tmp/tinyflux/**/*.csv", recursive=True):
    prev: dict[str, int] | None = None
    db = TinyFlux(log)
    measurement = MeasurementQuery()
    res = db.search(measurement == "weather")
    for row in res:
        now = row.time
        delta = obj_diff(prev, row.fields)
        prev = row.fields
        if len(delta):
            payload: dict[str, str | int] = {"time": now.isoformat(), **delta}
            logger.append(now, payload)

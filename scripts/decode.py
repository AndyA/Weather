import os
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import cached_property, reduce

import serial
from tinyflux import Point, TinyFlux

FIELDS = [
    ("c", 4),
    ("s", 4),
    ("g", 4),
    ("t", 4),
    ("r", 4),
    ("p", 4),
    ("h", 3),
    ("b", 6),
]


@dataclass(kw_only=True, frozen=True)
class Reading:
    line: str

    @property
    def body(self) -> str:
        return self.line[0:33]

    @property
    def checksum(self) -> int:
        return int(self.line[34:36], 16)

    @cached_property
    def computed_checksum(self) -> int:
        chars = [ord(c) for c in self.body]
        return reduce(lambda a, b: a ^ b, chars, 0)

    @property
    def valid(self) -> bool:
        return self.checksum == self.computed_checksum

    @cached_property
    def index(self) -> dict[str, int]:
        if not self.valid:
            raise ValueError("Invalid checksum")
        idx: dict[str, int] = {}
        pos = 0
        for t, w in FIELDS:
            slice = self.body[pos:][:w]
            if slice[0] != t:
                raise ValueError(f"Bad tag '{slice[0]}', expected '{t}'")
            idx[t] = int(slice[1:], 10)
            pos += w

        return idx


@dataclass(kw_only=True)
class Logger:
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


ser = serial.Serial(
    port="/dev/serial0",
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

logger = Logger(prefix="/data/logs/weather")

while line := ser.read_until():
    now = datetime.now(UTC)
    reading = Reading(line=line.decode("utf-8").strip())
    point = Point(time=now, measurement="weather", fields=reading.index)
    logger.db(now).insert(point)

import json
import os
from collections.abc import Generator
from dataclasses import dataclass
from datetime import UTC, datetime
from functools import cached_property, reduce
from typing import Any

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


@dataclass(kw_only=True, frozen=True)
class SerialSource:
    port: str

    @cached_property
    def _ser(self) -> serial.Serial:
        return serial.Serial(
            port=self.port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )

    def messages(self) -> Generator[str, Any]:
        while line := self._ser.read_until():
            yield line.decode("utf-8").strip()


@dataclass(kw_only=True, frozen=True)
class FileSource:
    name: str

    def messages(self) -> Generator[str, Any]:
        with open(self.name, "r") as f:
            for line in f:
                yield line.strip()


def obj_diff(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {k: v for k, v in b.items() if a[k] != v}


DRYRUN = False

if DRYRUN:
    source = FileSource(name="ref/weather.log")
    logger = Logger(prefix="tmp/logs")
else:
    source = SerialSource(port="/dev/serial0")
    logger = Logger(prefix="/data/logs/weather")

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
    diff: dict[str, str | int] = {"time": now.isoformat(), **delta}
    print(json.dumps(diff))

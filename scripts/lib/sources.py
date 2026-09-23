from collections.abc import Generator
from dataclasses import dataclass
from functools import cached_property
from typing import Any

import serial


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

from dataclasses import dataclass
from functools import cached_property, reduce

# c000s000g000t074r012p012h61b10080*36
# c000s000g005t074r012p012h59b10079*3E
# c000s001g009t074r012p012h59b10079*33
# c000s005g011t074r012p012h59b10079*3E
# c000s005g011t074r012p012h59b10080*38
# c000s006g011t074r012p012h59b10080*3B
# c045s000g005t074r012p012h59b10079*3F
# c045s000g007t074r012p012h59b10079*3D
#  234 234 234 234 234 234 23 23456


# c045
# s000
# g007
# t074
# r012
# p012
# h59
# b10079
# *3D


@dataclass(kw_only=True, frozen=True)
class Datum:
    tag: str
    value: int


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
            idx[t] = int(slice[1:])
            pos += w

        return idx


with open("ref/weather.log") as f:
    readings = [Reading(line=l.strip()) for l in f]

for r in readings:
    print(r.index)

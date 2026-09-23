import os
from dataclasses import dataclass
from datetime import datetime

from tinyflux import TinyFlux


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

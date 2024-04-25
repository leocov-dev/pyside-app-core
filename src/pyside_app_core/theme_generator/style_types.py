from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class QtResourceFile:
    path: str | Path
    alias: str | None = field(default=None)


@dataclass(frozen=True, kw_only=True)
class QtResourceGroup:
    prefix: str | None = field(default=None)
    lang: str | None = field(default=None)
    files: List[QtResourceFile] = field(default_factory=list)

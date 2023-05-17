from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class QtResourceFile:
    path: str | Path
    alias: str | None = None


@dataclass(frozen=True)
class QtResourceGroup:
    files: List[QtResourceFile]
    prefix: str | None = None
    lang: str | None = None

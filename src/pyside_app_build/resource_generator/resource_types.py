import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class QtResourceFile:
    path: str | Path
    alias: str | None


@dataclasses.dataclass(frozen=True)
class QtResourceGroup:
    prefix: str | None
    lang: str | None
    files: list[QtResourceFile]

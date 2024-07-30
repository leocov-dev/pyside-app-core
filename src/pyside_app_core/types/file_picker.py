from pathlib import Path
from typing import NamedTuple

from PySide6.QtWidgets import QFileDialog

_user_home = Path.home()


class DirConfig(NamedTuple):
    caption: str
    starting_directory: Path | None
    options: QFileDialog.Option | None


class FileConfig(NamedTuple):
    caption: str
    starting_directory: Path | None
    options: QFileDialog.Option | None
    selection_filter: str | None


DEFAULT_FILE_CONFIG = FileConfig(
    caption="Pick a file...",
    starting_directory=_user_home,
    options=QFileDialog.Option.ReadOnly,
    selection_filter="All Files (*)",
)
DEFAULT_DIR_CONFIG = DirConfig(
    caption="Pick a directory...",
    starting_directory=_user_home,
    options=QFileDialog.Option.ShowDirsOnly,
)

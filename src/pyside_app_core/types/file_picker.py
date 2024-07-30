from pathlib import Path
from typing import NamedTuple

from PySide6.QtWidgets import QFileDialog

_user_home = Path.home()


class DirConfig(NamedTuple):
    caption: str = "Pick a directory..."
    starting_directory: Path | None = None
    options: QFileDialog.Option | None = None


class FileConfig(NamedTuple):
    caption: str = "Pick a file..."
    starting_directory: Path | None = None
    options: QFileDialog.Option | None = None
    selection_filter: str | None = None


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

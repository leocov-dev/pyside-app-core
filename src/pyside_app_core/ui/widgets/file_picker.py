from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class FilePicker(QWidget):

    path_updated = Signal(Path)

    def __init__(
        self,
        *,
        heading: str = "",
        caption: str = "Pick a file...",
        starting_directory: Path = Path.home(),
        selection_filter: str = "All Files (*)",
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self._file_dialog = QFileDialog(
            parent=self,
            caption=caption,
            directory=str(starting_directory.expanduser().absolute()),
            filter=selection_filter,
        )

        # ---
        _ly = QHBoxLayout()
        _ly.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_ly)

        if heading:
            _ly.addWidget(QLabel(heading))

        self._file_path = QLineEdit(parent=self)
        _ly.addWidget(self._file_path)

        _btn = QPushButton("Browse")
        _ly.addWidget(_btn)

        # ---
        self._file_path.textChanged.connect(self._emit_path_change)
        _btn.clicked.connect(self._open_browser)

    @property
    def file_path(self) -> Path | None:
        text = self._file_path.text().strip()
        return Path(text) if text else None

    def set_file_path(self, file_path: Path | None) -> None:
        self._file_path.setText(str(file_path))

    def clear(self) -> None:
        self._file_path.clear()

    def _open_browser(self) -> None:
        self._file_dialog.exec()

    def _emit_path_change(self, text_path: str) -> None:
        if not text_path:
            self.path_updated.emit(None)

        path = Path(text_path)
        self.path_updated.emit(path if path.exists() else None)

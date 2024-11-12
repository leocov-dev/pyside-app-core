import os
from enum import Enum, auto
from pathlib import Path
from typing import cast

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from pyside_app_core import log
from pyside_app_core.types.file_picker import DEFAULT_DIR_CONFIG, DEFAULT_FILE_CONFIG, DirConfig, FileConfig


class FilePickerType(Enum):
    DIR = auto()
    FILE = auto()


class FilePicker(QWidget):
    path_updated = Signal(object)

    @property
    def valueChanged(self) -> Signal:
        return self.path_updated  # type: ignore[return-value]

    def __init__(
        self,
        *,
        heading: str = "",
        placeholder: str = "",
        config: DirConfig | FileConfig | FilePickerType | None = None,
        truncate_path: int = -1,
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._truncate_path = truncate_path

        # ---
        # true path
        self._file_path: Path | None = None

        # ---
        self._browse_config: FileConfig | DirConfig
        if isinstance(config, FilePickerType):
            self._browse_config = DEFAULT_FILE_CONFIG if config == FilePickerType.FILE else DEFAULT_DIR_CONFIG
        else:
            self._browse_config = config or DEFAULT_FILE_CONFIG

        # ---
        _ly = QHBoxLayout()
        _ly.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_ly)

        if heading:
            _ly.addWidget(QLabel(heading))

        # display only
        self._path_edit = QLineEdit(parent=self)
        self._path_edit.setClearButtonEnabled(True)
        if placeholder:
            self._path_edit.setPlaceholderText(placeholder)
        _ly.addWidget(self._path_edit)

        self._browse_btn = QPushButton("Browse")
        _ly.addWidget(self._browse_btn)

        # ---
        self._path_edit.textEdited.connect(self.set_file_path)
        self._browse_btn.clicked.connect(self._on_browse_btn_clicked)

    @property
    def file_path(self) -> Path | None:
        return self._file_path

    def set_file_path(self, file_path: Path | str | None) -> None:
        file_path = Path(file_path) if file_path else None

        log.debug(f"FilePicker.set_file_path({file_path})")
        self._file_path = file_path

        if self._truncate_path > 0 and self._file_path:
            parts = self._file_path.parts
            shortened = parts[-min(len(parts), self._truncate_path) :]
            if len(shortened) < len(parts):
                shortened = ("...", *shortened)
            self._path_edit.setText(os.sep.join(shortened))
        else:
            self._path_edit.setText(str(file_path or ""))

        self.path_updated.emit(self._file_path)

    def setReadOnly(self, value: bool = True) -> None:  # noqa: FBT002
        self._path_edit.setClearButtonEnabled(not value)
        self._path_edit.setReadOnly(value)
        self._browse_btn.setDisabled(value)
        self._browse_btn.setHidden(value)

    def setEnabled(self, value: bool = True) -> None:  # noqa: FBT002
        self._path_edit.setClearButtonEnabled(value)
        super().setEnabled(value)

    def setDisabled(self, value: bool = True) -> None:  # noqa: FBT002
        self._path_edit.setClearButtonEnabled(not value)
        super().setDisabled(value)

    def setValue(self, value: Path | str | None) -> None:
        self.set_file_path(value)

    def clear(self) -> None:
        self.set_file_path(None)

    def _on_browse_btn_clicked(self) -> None:
        starting_dir: Path | None

        if self._browse_config.starting_directory and not self._file_path:
            starting_dir = self._browse_config.starting_directory
        else:
            starting_dir = self.file_path if (self._file_path and cast(Path, self.file_path).exists()) else Path.home()

        if isinstance(self._browse_config, FileConfig):
            path, _ = QFileDialog.getOpenFileName(
                self,
                str(self._browse_config.caption),
                str(starting_dir),
                self._browse_config.selection_filter or "",
                "",
                self._browse_config.options or QFileDialog.Option.ReadOnly,
            )
        else:
            path = QFileDialog.getExistingDirectory(
                self,
                str(self._browse_config.caption),
                str(starting_dir),
                cast(QFileDialog.Option, self._browse_config.options),
            )

        if path:
            self.set_file_path(path)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication()

    fp = FilePicker()
    fp.show()

    app.exec()

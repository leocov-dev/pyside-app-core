import os
from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from pyside_app_core.types.file_picker import DEFAULT_FILE_CONFIG, DirConfig, FileConfig


class FilePicker(QWidget):
    path_updated = Signal(Path)

    @property
    def valueChanged(self) -> Signal:
        return self.path_updated  # type: ignore[return-value]

    def __init__(
        self,
        *,
        heading: str = "",
        config: DirConfig | FileConfig | None = None,
        truncate_path: int = -1,
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._truncate_path = truncate_path

        # ---
        # true path
        self._file_path: Path | None = None

        # ---
        self._browse_config = config or DEFAULT_FILE_CONFIG

        # ---
        _ly = QHBoxLayout()
        _ly.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_ly)

        if heading:
            _ly.addWidget(QLabel(heading))

        # display only
        self._path_edit = QLineEdit(parent=self)
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
        self._file_path = file_path if file_path is None else Path(file_path)

        if self._truncate_path > 0 and self._file_path is not None:
            parts = self._file_path.parts
            shortened = parts[-min(len(parts), self._truncate_path) :]
            if len(shortened) < len(parts):
                shortened = ("...", *shortened)
            self._path_edit.setText(os.sep.join(shortened))
        else:
            self._path_edit.setText(str(file_path or ""))

        self.path_updated.emit(self._file_path)

    def setValue(self, value: Path | str | None) -> None:
        self.set_file_path(value)

    def clear(self) -> None:
        self.set_file_path(None)

    def setReadOnly(self, val: bool = True) -> None:  # noqa: FBT002
        self._path_edit.setReadOnly(val)
        self._browse_btn.setDisabled(val)
        self._browse_btn.setHidden(val)

    def _on_browse_btn_clicked(self) -> None:
        kwargs: dict[str, Any] = {
            "caption": self._browse_config.caption,
        }
        if self._browse_config.starting_directory:
            kwargs["dir"] = self._browse_config.starting_directory
        if self._browse_config.options:
            kwargs["options"] = self._browse_config.options

        if isinstance(self._browse_config, FileConfig):
            if self._browse_config.selection_filter:
                kwargs["filter"] = self._browse_config.selection_filter

            path, _ = QFileDialog.getOpenFileName(
                self,
                str(kwargs.get("caption")),
                str(kwargs.get("dir", "")),
                kwargs.get("filter", ""),
                "",
                cast(QFileDialog.Option, kwargs.get("options")),
            )
        else:
            path = QFileDialog.getExistingDirectory(
                self,
                str(kwargs.get("caption")),
                str(kwargs.get("dir")),
                cast(QFileDialog.Option, kwargs.get("options")),
            )

        self.set_file_path(path)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication()

    fp = FilePicker()
    fp.show()

    app.exec()

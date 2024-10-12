from typing import Any, Protocol

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QDoubleSpinBox, QFileDialog, QHBoxLayout, QLineEdit, QSpinBox, QWidget

# from pyside_app_core.services.preferences_service import PrefItem
from pyside_app_core.types.file_picker import DirConfig, FileConfig
from pyside_app_core.ui.widgets.file_picker import FilePicker


class PrefItem(Protocol):
    @property
    def value(self) -> Any: ...

    def set_value(self, value: Any) -> None: ...


class ItemWidget(QWidget):
    def __init__(self, item: PrefItem, parent: QWidget | None = None):
        super().__init__(parent)
        self._item = item

        ly = QHBoxLayout()
        ly.setContentsMargins(0, 0, 0, 0)
        self.setLayout(ly)


class _StringItemWidget(ItemWidget):
    def __init__(self, item: PrefItem, parent: QWidget | None = None):
        super().__init__(item, parent)

        le = QLineEdit(item.value, parent=self)
        self.layout().addWidget(le)

        le.textChanged.connect(item.set_value)


class _IntItemWidget(ItemWidget):
    def __init__(self, item: PrefItem, parent: QWidget | None = None):
        super().__init__(item, parent)

        sb = QSpinBox(parent=self)
        sb.setValue(item.value)
        self.layout().addWidget(sb)

        sb.valueChanged.connect(item.set_value)


class _FloatItemWidget(ItemWidget):
    def __init__(self, item: PrefItem, parent: QWidget | None = None):
        super().__init__(item, parent)

        sb = QDoubleSpinBox(parent=self)
        sb.setValue(item.value)
        self.layout().addWidget(sb)

        sb.valueChanged.connect(item.set_value)


class _BoolItemWidget(ItemWidget):
    def __init__(self, item: PrefItem, parent: QWidget | None = None):
        super().__init__(item, parent)

        cb = QCheckBox(parent=self)
        cb.setCheckState(Qt.CheckState.Checked if item.value else Qt.CheckState.Unchecked)
        self.layout().addWidget(cb)

        cb.checkStateChanged.connect(item.set_value)


class _PathItemWidget(ItemWidget):
    def __init__(self, item: PrefItem, parent: QWidget | None = None):
        super().__init__(item, parent)

        path = item.value
        config: DirConfig | FileConfig
        if path.is_dir():
            config = DirConfig(
                caption="Pick a directory", starting_directory=path, options=QFileDialog.Option.ShowDirsOnly
            )
        else:
            config = FileConfig(
                caption="Pick a file...",
                starting_directory=path,
                options=QFileDialog.Option.ReadOnly,
                selection_filter="All Files (*)",
            )

        fp = FilePicker(
            config=config,
            parent=self,
        )
        fp.set_file_path(item.value)
        self.layout().addWidget(fp)

        fp.valueChanged.connect(item.set_value)
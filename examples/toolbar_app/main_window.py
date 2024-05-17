from PySide6.QtCore import QSize
from PySide6.QtWidgets import QLabel, QVBoxLayout

from pyside_app_core.qt.standard import MainWindow
from pyside_app_core.qt.widgets.connection_manager import ConnectionManager
from pyside_app_core.qt.widgets.core_icon import CoreIcon
from pyside_app_core.qt.widgets.multi_combo_box import MultiComboBox


class SimpleMainWindow(MainWindow):
    def __init__(self) -> None:
        super().__init__()

        # ------------------------------------------------------------------------------
        self.setMinimumSize(QSize(480, 240))

        _tool_bar = self.addToolBar("main")
        _tool_bar.setObjectName("main-tool-bar")
        plug_action = _tool_bar.addAction(
            CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
            "Connect",
        )
        plug_action.setCheckable(True)
        plug_action2 = _tool_bar.addAction(
            CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
            "Connect",
        )
        plug_action2.setCheckable(True)
        plug_action2.setChecked(True)
        reload_action = _tool_bar.addAction(
            CoreIcon(
                ":/core/iconoir/refresh-circle.svg",
            ),
            "Reload",
        )
        reload_action.setDisabled(True)
        _raise_action = _tool_bar.addAction(
            CoreIcon(
                ":/core/iconoir/floppy-disk.svg",
            ),
            "Save",
        )

        def _raise() -> None:
            raise Exception("This is a test error")  # noqa

        _raise_action.triggered.connect(_raise)

        # -----
        _central_layout = QVBoxLayout()
        self.centralWidget().setLayout(_central_layout)

        _heading = QLabel("Examples")
        _central_layout.addWidget(_heading)

        _multi_combo = MultiComboBox[str](placeholder_text="Options", parent=self)
        _multi_combo.addItems(["one", "two", "three", "four"])
        _central_layout.addWidget(_multi_combo)

        _con_mgr = ConnectionManager(parent=self)
        _central_layout.addWidget(_con_mgr)

        _central_layout.addStretch()

        self.statusBar().showMessage("Hi There")

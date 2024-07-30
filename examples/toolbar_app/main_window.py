from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLabel, QVBoxLayout

from pyside_app_core.services.preferences_service import PreferencesService
from pyside_app_core.types.preferences import Pref, PrefsConfig, PrefsGroup
from pyside_app_core.ui.standard import MainWindow
from pyside_app_core.ui.widgets.connection_manager import ConnectionManager
from pyside_app_core.ui.widgets.core_icon import CoreIcon
from pyside_app_core.ui.widgets.multi_combo_box import MultiComboBox
from pyside_app_core.ui.widgets.preferences_manager import PreferencesManager


class SimpleMainWindow(MainWindow):
    def __init__(self) -> None:
        super().__init__(primary=True)

        # ------------------------------------------------------------------------------
        self.setMinimumSize(QSize(480, 240))

        self._prefs_mgr: PreferencesManager | None = None
        self._preferences = PrefsConfig(
            PrefsGroup(
                "Application",
                [
                    Pref("Remember Position", True),
                    Pref("Remember Size", True),
                    Pref("Default Path", Path.home() / "one" / "two" / "three" / "four"),
                ],
            ),
            PrefsGroup(
                "Developer",
                [
                    Pref("Debug Mode", False),
                ],
            ),
        )
        PreferencesService.load_config(self._preferences)

        self._menus()
        self._content()

    def _menus(self) -> None:
        with (
            self._menu_bar.menu("File") as file_menu,
            file_menu.action("Preferences...") as prefs_action,
        ):
            prefs_action.setMenuRole(QAction.MenuRole.PreferencesRole)
            prefs_action.triggered.connect(self._open_preferences)

    def _content(self) -> None:
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

    def _open_preferences(self) -> None:
        if self._prefs_mgr:
            self._prefs_mgr.close()

        self._prefs_mgr = PreferencesManager(self._preferences)
        self._prefs_mgr.show()

from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLabel, QVBoxLayout

from pyside_app_core import log
from pyside_app_core.services.preferences_service import PreferencesService, PrefGroup, PrefItem, PrefSection
from pyside_app_core.ui.standard import MainWindow
from pyside_app_core.ui.widgets.connection_manager import ConnectionManager
from pyside_app_core.ui.widgets.core_icon import CoreIcon
from pyside_app_core.ui.widgets.multi_combo_box import MultiComboBox
from pyside_app_core.ui.widgets.preferences_manager import PreferencesManager
from pyside_app_core.ui.widgets.tool_bar_ctx import ToolBarContext


class SimpleMainWindow(MainWindow):
    def __init__(self) -> None:
        super().__init__(primary=True)

        # ------------------------------------------------------------------------------
        self.setMinimumSize(QSize(480, 240))

        self._prefs_mgr: PreferencesManager | None = None
        PreferencesService.add_prefs(
            PrefSection(
                "Application",
                "app",
                [
                    PrefGroup(
                        "Keep Between Sessions",
                        "remember",
                        [
                            PrefItem.new("Remember Position", "pos", True),
                            PrefItem.new("Remember Size", "size", False),
                            PrefItem.new("Remember Number", "float-num", 12.34),
                        ],
                    ),
                    PrefGroup(
                        "Paths",
                        "paths",
                        [
                            PrefItem.new("Default Path", "path", Path.home() / "one" / "two" / "three" / "four"),
                            PrefItem.new(
                                "Another Path", "another-path", Path.home() / "one" / "two" / "three" / "file.txt"
                            ),
                        ],
                    ),
                ],
            ),
            PrefGroup(
                "Developer",
                "dev",
                [
                    PrefItem.new("Debug Mode", "debug", False),
                    PrefItem.new("Debug Format", "debug-fmt", "some-format-string"),
                    PrefItem.new("Debug Level", "debug-lvl", 0),
                ],
            ),
        )

        log.debug(PreferencesService.instance())

        self._menus()
        self._content()

    def _menus(self) -> None:
        with (
            self._menu_bar.menu("File") as file_menu,
            file_menu.action("Preferences...") as prefs_action,
        ):
            prefs_action.setMenuRole(QAction.MenuRole.PreferencesRole)
            prefs_action.triggered.connect(PreferencesManager.open)

    def _content(self) -> None:
        _tool_bar = ToolBarContext("top", self)
        _tool_bar.setObjectName("main-tool-bar")

        with _tool_bar.add_action(
            "Connect",
            CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
        ) as plug_action:
            plug_action.setCheckable(True)

        with _tool_bar.add_action(
            "Connect",
            CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
        ) as plug_action:
            plug_action.setCheckable(True)
            plug_action.setChecked(True)

        with _tool_bar.add_action(
            "Reload",
            CoreIcon(
                ":/core/iconoir/refresh-circle.svg",
            ),
        ) as reload_action:
            reload_action.setDisabled(True)

        with _tool_bar.add_action(
            "Save",
            CoreIcon(
                ":/core/iconoir/floppy-disk.svg",
            ),
        ) as raise_action:

            def _raise() -> None:
                raise Exception("This is a test error")  # noqa

            raise_action.triggered.connect(_raise)

        _tool_bar.add_stretch()

        with _tool_bar.add_action(
            "Preferences",
            CoreIcon(
                ":/core/iconoir/settings.svg",
            ),
        ) as prefs_action:
            prefs_action.triggered.connect(PreferencesManager.open)

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

    def open_preferences(self) -> None:
        if self._prefs_mgr:
            self._prefs_mgr.close()

        self._prefs_mgr = PreferencesManager()
        self._prefs_mgr.show()

from pathlib import Path

from loguru import logger
from PySide6.QtGui import Qt

from pyside_app_core.app import AppMetadata
from pyside_app_core.errors import excepthook
from pyside_app_core.log import configure_get_logger_func
from pyside_app_core.services.preferences_service import PreferencesService, PrefGroup, PrefItem, PrefSection
from pyside_app_core.ui.prefs import ComboItemWidget, PathWithPlaceholder
from pyside_app_core.ui.standard.error_dialog import ErrorDialog
from pyside_app_core.ui.widgets.base_app import BaseApp
from pyside_app_core.ui.widgets.file_picker import FilePickerType
from toolbar_app import __version__
from toolbar_app.main_window import ToolbarAppMainWindow

configure_get_logger_func(lambda: logger)

excepthook.install_excepthook(ErrorDialog)
AppMetadata.init(
    "com.example.simple-app",
    "Simple App",
    __version__,
    icon_resource=":/tb/app/icon.png",
    help_url="https://github.com/leocov-dev/pyside-app-core",
    bug_report_url="https://github.com/leocov-dev/pyside-app-core/issues",
)


class SimpleApp(BaseApp):
    def __init__(self, resources_rcc: Path | None = None):
        super().__init__(resources_rcc=resources_rcc)

        # ----
        PreferencesService.connect_pref_changed(
            "app.settings.theme",
            lambda p: self.styleHints().setColorScheme(Qt.ColorScheme(p.value)),
        )

        # self.styleHints().setColorScheme(Qt.ColorScheme(PreferencesService.fqdn_to_pref("app.settings.theme").value))

    def configure_preferences(self) -> None:
        PreferencesService.add_prefs(
            PrefSection(
                "Application",
                "app",
                [
                    PrefGroup(
                        "Settings",
                        "settings",
                        [PrefItem.new("Theme", "theme", 0, widget_class=ComboItemWidget(["System", "Dark", "Light"]))],
                    ),
                    PrefGroup(
                        "Keep Between Sessions",
                        "remember",
                        [
                            PrefItem.new("Remember Position", "pos", True),
                            PrefItem.new("Remember Size", "size", False),
                            PrefItem.new("Remember Number", "float-num", 12.34),
                            PrefItem.new(
                                "Special Choice",
                                "spec-choice",
                                1,
                                widget_class=ComboItemWidget(["One", "Two", "Three"]),
                            ),
                        ],
                    ),
                    PrefGroup(
                        "Paths",
                        "paths",
                        [
                            PrefItem.new(
                                "Default Path",
                                "path",
                                Path(),
                                widget_class=PathWithPlaceholder(
                                    placeholder_text="my placeholder...",
                                    kind=FilePickerType.DIR,
                                ),
                            ),
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
                    PrefItem.new(
                        "My Selection",
                        "my-sel",
                        0,
                        widget_class=ComboItemWidget(["A", "B", "C", "D", "E"]),
                    ),
                ],
            ),
        )

    def build_main_window(self):
        return ToolbarAppMainWindow()

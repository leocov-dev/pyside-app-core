from pathlib import Path

from pyside_app_core.qt.widgets.base_app import BaseApp
from toolbar_app.main_window import SimpleMainWindow


class SimpleApp(BaseApp):
    def __init__(self, resources_rcc: Path | None = None):
        super().__init__(resources_rcc=resources_rcc)

    def build_main_window(self):
        return SimpleMainWindow()

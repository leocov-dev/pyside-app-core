from pathlib import Path

from pyside_app_core.qt.widgets.base_app import BaseApp
from toolbar_app.main_window import SimpleMainWindow


class SimpleApp(BaseApp):
    def __init__(self, resources_rcc: Path | None = None):
        super(SimpleApp, self).__init__(resources_rcc=resources_rcc)

        self._main_window = SimpleMainWindow()
        self._main_window.close_window.connect(lambda: self.exit(0))

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from pyside_app_core.errors.basic_errors import ApplicationError
from pyside_app_core.qt.util.style_sheet import (
    apply_style_sheet,
    register_resource_file,
)


class BaseApp(QApplication):
    def __init__(self, resources_rcc: Path | None = None, *args, **kwargs):
        super(BaseApp, self).__init__(*args, **kwargs)
        self.setStyle("Fusion")
        self.setAttribute(
            Qt.ApplicationAttribute.AA_UseStyleSheetPropagationInWidgetStyles
        )

        register_resource_file(resources_rcc)

        apply_style_sheet(":/style.qss", self)

        # override in subclass
        self._main_window = None

    def launch(self) -> int:
        if not self._main_window:
            raise ApplicationError(
                f"Must subclass {self.__class__.__name__} and define a main window"
            )

        self._main_window.show()
        return self.exec()

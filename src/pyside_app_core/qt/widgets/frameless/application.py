from pathlib import Path

from PySide6.QtCore import QFile, QResource, Qt, QTextStream
from PySide6.QtWidgets import QApplication

from pyside_app_core.errors.basic_errors import ApplicationError


class FramelessApp(QApplication):
    def __init__(self, resources_rcc: Path):
        super(FramelessApp, self).__init__()
        self.setAttribute(
            Qt.ApplicationAttribute.AA_UseStyleSheetPropagationInWidgetStyles
        )

        # registering a binary rcc is marginally faster than importing a python resource module
        QResource.registerResource(str(resources_rcc))

        self.setStyle("Fusion")

        qss_file = QFile(":/style.qss")
        qss_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        ts = QTextStream(qss_file)
        self.setStyleSheet(ts.readAll())

        # override in subclass
        self._main_window = None

    def launch(self) -> int:
        if not self._main_window:
            raise ApplicationError(f"Must subclass {self.__class__.__name__} and define a main window")

        self._main_window.show()
        return self.exec()

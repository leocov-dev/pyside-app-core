import sys
from pathlib import Path
from typing import Generic, TypeVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QStyle

from pyside_app_core import log
from pyside_app_core.errors.basic_errors import ApplicationError
from pyside_app_core.qt import register_resource_file
from pyside_app_core.qt.application_service import AppMetadata

M = TypeVar("M", bound=QMainWindow)


class BaseApp(QApplication, Generic[M]):
    def __init__(self, resources_rcc: Path | None = None, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.setStyle("fusion")
        self.setAttribute(Qt.ApplicationAttribute.AA_UseStyleSheetPropagationInWidgetStyles)

        register_resource_file(resources_rcc)

        self.setWindowIcon(
            QIcon(AppMetadata.icon)
            if AppMetadata.icon
            else self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )

        self._main_window: M = self.build_main_window()

    def build_main_window(self) -> M:
        raise NotImplementedError

    def launch(self) -> None:
        if not self._main_window:
            raise ApplicationError(f"Must subclass {BaseApp.__name__} and define a main window")

        self._main_window.show()

        try:
            self.about_to_exit(self.exec())
        except Exception as e:  # noqa:BLE001
            log.exception(e)
            sys.exit(1)

    def about_to_exit(self, ret_code: int) -> int:
        return ret_code

import sys
from pathlib import Path
from typing import Generic, TypeVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QStyle

from pyside_app_core import log
from pyside_app_core.app.application_service import AppMetadata
from pyside_app_core.errors.basic_errors import ApplicationError
from pyside_app_core.ui import register_resource_file

M = TypeVar("M", bound=QMainWindow)


class BaseApp(QApplication, Generic[M]):
    def __init__(
        self,
        resources_rcc: Path | None = None,
        *args: object,
        **kwargs: object,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.setStyle("fusion")
        self.setAttribute(Qt.ApplicationAttribute.AA_UseStyleSheetPropagationInWidgetStyles)

        register_resource_file(resources_rcc)

        self.setApplicationName(AppMetadata.name.replace(" ", "-"))
        self.setApplicationDisplayName(AppMetadata.name)
        self.setOrganizationName(AppMetadata.id)
        self.setApplicationVersion(AppMetadata.version)

        self.setWindowIcon(
            QIcon(AppMetadata.icon)
            if AppMetadata.icon
            else self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )

        self._main_window: M = self.build_main_window()

    def build_main_window(self) -> M:
        raise NotImplementedError

    def on_show_main_window(self) -> None:
        pass

    def launch(self) -> None:
        if not self._main_window:
            raise ApplicationError(f"Must subclass {BaseApp.__name__} and define a main window")

        self._main_window.show()
        self.on_show_main_window()

        try:
            self.about_to_exit(self.exec())
        except Exception as e:  # noqa:BLE001
            log.exception(e)
            sys.exit(1)

    def before_exit(self) -> None:
        pass

    def about_to_exit(self, ret_code: int) -> int:
        self.before_exit()
        return ret_code

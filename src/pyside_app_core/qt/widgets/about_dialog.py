from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel

from pyside_app_core.qt.widgets.frameless.base_dialog import (
    FramelessBaseDialog,
    StandardButton,
)
from pyside_app_core.services import application_service


class AboutDialog(FramelessBaseDialog):
    def __init__(self):
        super().__init__(icon=QIcon(":/std/icons/console"))

        self.setFixedSize(500, 300)
        self.setWindowTitle(f"About {application_service.get_app_name()}")

        self.setStandardButtons(StandardButton.Close)
        self.setDefaultButton(StandardButton.Close)

        _version = QLabel(f"Version {application_service.get_app_version()}")
        self.addWidget(_version)

        self.addStretch()

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel, QVBoxLayout

from pyside_app_core.frameless.main_toolbar_window import FramelessMainToolbarWindow


class SimpleMainWindow(FramelessMainToolbarWindow):
    def __init__(self):
        super(SimpleMainWindow, self).__init__()

        # ------------------------------------------------------------------------------
        self.setMinimumSize(QSize(480, 240))

        _central_layout = QVBoxLayout()
        self.centralWidget().setLayout(_central_layout)

        _heading = QLabel(self.tr("Examples"))
        _central_layout.addWidget(_heading)

        _central_layout.addStretch()

        for _ in range(15):
            with self._tool_bar.add_action(
                self.tr("error dialog"), QIcon(":/std/icons/console")
            ) as ed:

                def _show_ed():
                    raise ValueError("A simulated error")

                ed.triggered.connect(_show_ed)

        self.statusBar().showMessage(self.tr("Hi There"))

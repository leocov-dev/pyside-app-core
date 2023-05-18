from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QApplication, QLabel, QPlainTextEdit

from pyside_app_core.qt.widgets.frameless.base_dialog import (
    FramelessBaseDialog,
    StandardButton,
)


class ErrorDialog(FramelessBaseDialog):
    def __init__(self, message: str, detailed: str | None = None):
        super().__init__()

        self.setWindowTitle("Encountered An Unexpected Error")
        self.setMinimumWidth(640)

        self._clipboard = QClipboard(parent=self)

        self.setStandardButtons(
            StandardButton.Ignore | StandardButton.Reset | StandardButton.Abort
        )
        self.setDefaultButton(StandardButton.Ignore)

        self.setButtonText(StandardButton.Ignore, "Ignore")
        self.setButtonText(StandardButton.Reset, "Copy")
        self.setButtonText(StandardButton.Abort, "Quit")

        _copy_btn = self.button(StandardButton.Reset)
        _copy_btn.clicked.connect(self._copy_to_clipboard)

        _quit_btn = self.button(StandardButton.Abort)
        _quit_btn.clicked.connect(QApplication.instance().quit)

        _m_lab = QLabel("Message:")
        self.addWidget(_m_lab)
        self._message_box = QPlainTextEdit(message, parent=self)
        self._message_box.setReadOnly(True)
        self.addWidget(self._message_box)

        self._trace_box = None
        if detailed:
            _t_lab = QLabel("Details:")
            self.addWidget(_t_lab)
            self._trace_box = QPlainTextEdit(detailed, parent=self)
            self._trace_box.setReadOnly(True)
            self.addWidget(self._trace_box)

    def _copy_to_clipboard(self):
        if self._trace_box:
            self._clipboard.setText(
                f"{self._message_box.toPlainText()}\n\n{self._trace_box.toPlainText()}"
            )
        else:
            self._clipboard.setText(self._message_box.toPlainText())

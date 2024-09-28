from PySide6.QtWidgets import QMessageBox, QWidget

from pyside_app_core.utils import strings


class ErrorDialog(QMessageBox):
    CHAR_WIDTH = 120

    def __init__(
        self,
        etype: type[BaseException],
        msg: str,
        details: str,
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Error")
        self.setIcon(QMessageBox.Icon.Critical)

        self.setText(f"Error: {etype.__name__: <{self.CHAR_WIDTH}}")
        if msg:
            self.setInformativeText(strings.wrap_text(msg, width=self.CHAR_WIDTH, padded=True) + "\n")
        if details:
            self.setDetailedText(details)

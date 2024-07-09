from PySide6 import QtWidgets

from pyside_app_core.utils import strings


class ErrorDialog(QtWidgets.QMessageBox):
    CHAR_WIDTH = 120

    def __init__(
        self,
        etype: type[BaseException],
        msg: str,
        details: str,
        parent: QtWidgets.QWidget | None = None,
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Error")

        self.setText(f"Error: {etype.__name__: <{self.CHAR_WIDTH}}")
        if msg:
            self.setInformativeText(strings.wrap_text(msg, width=self.CHAR_WIDTH, padded=True) + "\n")
        if details:
            self.setDetailedText(details)

from PySide6.QtCore import QObject, QRegularExpression
from PySide6.QtGui import QValidator


class FloatValidator(QValidator):
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent=parent)

    def validate(self, input_string: str, _: int) -> QValidator.State:
        regexp = QRegularExpression(r"^[0-9]*(\.[0-9]*)?$")

        if regexp.match(input_string).hasMatch():
            return QValidator.State.Acceptable

        return QValidator.State.Invalid

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget

from pyside_app_core.services import application_service


class FramelessWindowShade(QWidget):
    def __init__(
        self,
        parent: QWidget,
    ):
        super(FramelessWindowShade, self).__init__(parent=parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._theme = application_service.get_app_theme()
        self._disabled = False

    def setDisabled(self, val: bool) -> None:
        self._disabled = val

    def setEnabled(self, val: bool) -> None:
        self.setDisabled(not val)

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = self.parent().contentsRect()
        self.setFixedSize(rect.size())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(Qt.GlobalColor.transparent))
        p.setBrush(QBrush(Qt.GlobalColor.transparent))

        if not self.isActiveWindow():
            p.setPen(QPen(Qt.GlobalColor.transparent))
            bkgd_color = self._theme.background_color.darker(125)
            bkgd_color.setAlpha(80)
            p.setBrush(QBrush(bkgd_color))
            p.drawRoundedRect(
                rect, self._theme.win_corner_radius, self._theme.win_corner_radius
            )

        p.end()

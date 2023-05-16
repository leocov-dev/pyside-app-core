from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget

from pyside_app_core.services import application_service


class FramelessWindowBorder(QWidget):
    def __init__(
        self,
        parent: QWidget,
    ):
        super(FramelessWindowBorder, self).__init__(parent=parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._theme = application_service.get_app_theme()
        self._corner_rounding = self._theme.win_corner_radius
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

        if self._disabled:
            p.setPen(QPen(Qt.GlobalColor.transparent))
            p.setBrush(QBrush(QColor(40, 40, 40, 200)))
            p.drawRect(rect)

        # outline
        p.setBrush(QBrush(Qt.GlobalColor.transparent))

        draw_rect = rect.adjusted(1, 1, -1, -1)

        top_corner = QPainterPath(rect.topRight())
        top_corner.lineTo(rect.topLeft())
        top_corner.lineTo(rect.bottomLeft())
        p.setClipPath(top_corner)

        p.setPen(QPen(self._theme.background_color.lighter(220), 1))
        p.drawRoundedRect(
            draw_rect,
            self._theme.win_corner_radius - 2,
            self._theme.win_corner_radius - 2,
        )

        bottom_corner = QPainterPath(rect.topRight())
        bottom_corner.lineTo(rect.bottomRight())
        bottom_corner.lineTo(rect.bottomLeft())
        p.setClipPath(bottom_corner)

        p.setPen(QPen(self._theme.background_color.lighter(130), 2))
        p.drawRoundedRect(
            draw_rect,
            self._theme.win_corner_radius - 2,
            self._theme.win_corner_radius - 2,
        )

        p.end()

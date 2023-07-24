from enum import IntEnum
from typing import Callable, NamedTuple, Tuple

from PySide6.QtCore import QEvent, QLine, QPoint, QRect, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QResizeEvent,
)
from PySide6.QtWidgets import QWidget

from pyside_app_core.services import application_service, platform_service


class Action(IntEnum):
    NONE = 0
    CLOSE = 1
    MINIMIZE = 2
    MAXIMIZE = 3


ShapeFunc = Callable[[QPainter, QRect, QColor, Action], None]
EnabledFunc = Callable[[], bool]


class ButtonData(NamedTuple):
    color: QColor
    action: Action
    signal: Signal
    shape_fn: ShapeFunc
    enabled_fn: EnabledFunc


class WindowActions(QWidget):
    close_clicked = Signal()
    minimize_clicked = Signal()
    maximize_clicked = Signal()

    def __init__(
        self,
        parent: QWidget,
    ):
        super(WindowActions, self).__init__(parent=parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setContentsMargins(10, 12, 0, 0)

        self._theme = application_service.get_app_theme()
        self._hover = Action.NONE
        self._press = Action.NONE

        self._pen = QPen(Qt.GlobalColor.transparent)

        self._brush = QBrush(Qt.GlobalColor.transparent)

        _top_offset = self.contentsMargins().top() if platform_service.is_macos else 0
        self._side_offset = (
            self.contentsMargins().left()
            if platform_service.is_macos
            else self.contentsMargins().right()
        )

        if platform_service.is_macos:
            _width = 14
            _height = 14
            _spacing = 5
        elif platform_service.is_windows:
            _width = 45
            _height = 35
            _spacing = 3
        else:
            _width = 20
            _height = 20
            _spacing = 10

        self._a_rect = QRect(self._side_offset, _top_offset, _width, _height)
        self._b_rect = self._a_rect.translated(_width + _spacing, 0)
        self._c_rect = self._b_rect.translated(_width + _spacing, 0)

        if platform_service.is_macos:
            self.container_height = (
                self._a_rect.y() + self._a_rect.height() + self.contentsMargins().top()
            )
        elif platform_service.is_windows:
            self.container_height = self._a_rect.y() + self._a_rect.height()
        else:
            self.container_height = (
                self._a_rect.y()
                + self._a_rect.height()
                + self.contentsMargins().top() * 2
            )

        self.container_width = self._c_rect.x() + self._c_rect.width()

        self.setFixedHeight(self.container_height)
        self.setFixedWidth(self.container_width)

        _rect_list = [
            self._a_rect,
            self._b_rect,
            self._c_rect,
        ]

        _button_data = [
            ButtonData(
                self._theme.win_minimize,
                Action.MINIMIZE,
                self.minimize_clicked,
                self._draw_min,
                lambda: (
                    self.parent().windowFlags() & Qt.WindowType.WindowMinimizeButtonHint
                )
                > 0,
            ),
            ButtonData(
                self._theme.win_maximize,
                Action.MAXIMIZE,
                self.maximize_clicked,
                self._draw_max,
                lambda: (
                    self.parent().windowFlags() & Qt.WindowType.WindowMaximizeButtonHint
                )
                > 0,
            ),
            ButtonData(
                self._theme.win_close,
                Action.CLOSE,
                self.close_clicked,
                self._draw_close,
                lambda: (
                    self.parent().windowFlags() & Qt.WindowType.WindowCloseButtonHint
                )
                > 0,
            ),
        ]

        _order = [2, 0, 1] if platform_service.is_macos else [0, 1, 2]

        self._rect_map = []
        for i, o in enumerate(_order):
            self._rect_map.append((_rect_list[i], _button_data[o]))

    def paintEvent(self, event: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.GlobalColor.transparent)
        p.setBrush(Qt.GlobalColor.transparent)

        for rect, data in self._rect_map:
            enabled = self.isActiveWindow() and data.enabled_fn()

            self._draw_button(p, rect, data.color, data.action, enabled)

            if platform_service.is_macos and not enabled:
                pass
            else:
                c_shape = data.color if enabled else data.color.darker(300)
                c_shape = c_shape.darker(200) if platform_service.is_macos else c_shape
                data.shape_fn(p, rect, c_shape, data.action)

        p.end()

        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        prev = self._hover
        for rect, data in self._rect_map:
            if not data.enabled_fn():
                continue

            if rect.contains(event.pos()):
                self._hover = data.action
                break
        else:
            self._hover = Action.NONE

        if self._hover != prev:
            # repaint only on hover change
            self.update()

        super().mouseMoveEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._hover = Action.NONE
        self.update()

        super().leaveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        for rect, data in self._rect_map:
            if not data.enabled_fn():
                continue

            if rect.contains(event.pos()):
                data.signal.emit()
                break

        self._press = Action.NONE

        self.update()

        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        for rect, data in self._rect_map:
            if not data.enabled_fn():
                continue

            if rect.contains(event.pos()):
                self._press = data.action
                break
        else:
            self._press = Action.NONE

        self.update()

        super().mousePressEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if platform_service.is_macos:
            pass
        elif platform_service.is_windows:
            win_width = self.window().width()
            self.setGeometry(win_width - self.width(), 0, self.width(), self.height())
        else:
            win_width = self.window().width()
            self.setGeometry(
                win_width - self.width() - self.contentsMargins().left(),
                self.contentsMargins().top(),
                self.width(),
                self.height(),
            )

        super().resizeEvent(event)

    def _get_button_color(self, color: QColor, is_enabled: bool) -> QColor:
        if platform_service.is_windows:
            return QColor(Qt.GlobalColor.transparent)
        else:
            return color if is_enabled else self._theme.win_action_inactive

    def _draw_button(
        self, p: QPainter, rect: QRect, color: QColor, action: Action, enabled: bool
    ):
        p.setPen(Qt.GlobalColor.transparent)

        f_col = self._get_button_color(color, enabled)

        if enabled:
            if self._hover == action:
                f_col = color
            if self._press == action:
                f_col = color.lighter(135)

        p.setBrush(f_col)

        if platform_service.is_windows:
            if action == Action.CLOSE:
                offset = QPoint(0, 1)
                path = QPainterPath(rect.topLeft() + offset)
                path.lineTo(rect.bottomLeft() + offset)
                path.lineTo(rect.bottomRight() + offset)

                a = rect.topRight() + offset + QPoint(0, self._theme.win_corner_radius)
                b = rect.topRight() + offset - QPoint(self._theme.win_corner_radius, 0)

                path.lineTo(a)
                path.cubicTo(rect.topRight(), b, b)

                path.lineTo(rect.topLeft() + offset)
                p.drawPath(path)
            else:
                p.drawRect(rect)
        else:
            p.drawEllipse(rect)

    def _get_shape_tools(self, color: QColor, action: Action) -> Tuple[QPen, QBrush]:
        if self._press == action:
            color = color if platform_service.is_macos else color.lighter(200)
        elif self._hover == action:
            color = color if platform_service.is_macos else color.lighter()
        else:
            color = Qt.GlobalColor.transparent if platform_service.is_macos else color

        pen = QPen(color)
        pen.setWidth(3 if platform_service.is_windows else 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        brush = QBrush(color)

        return pen, brush

    def _scale_rect(self, rect: QRect, sw: int | float, sh: int | float) -> QRect:
        w = rect.width() * sh
        h = rect.height() * sw

        return rect.adjusted(w, h, -w, -h)

    def _draw_close(self, p: QPainter, rect: QRect, color: QColor, action: Action):
        pen, brush = self._get_shape_tools(color, action)
        p.setPen(pen)

        oH = (
            0.3
            if platform_service.is_macos
            else 0.325
            if platform_service.is_windows
            else 0.35
        )
        oW = (
            0.3
            if platform_service.is_macos
            else 0.375
            if platform_service.is_windows
            else 0.35
        )

        rect = self._scale_rect(rect.adjusted(1, 1, 0, 0), oH, oW)

        p.drawLines(
            [
                QLine(rect.topLeft(), rect.bottomRight()),
                QLine(rect.bottomLeft(), rect.topRight()),
            ]
        )

    def _draw_max(self, p: QPainter, rect: QRect, color: QColor, action: Action):
        pen, brush = self._get_shape_tools(color, action)
        p.setPen(pen)

        oH = (
            0.3
            if platform_service.is_macos
            else 0.325
            if platform_service.is_windows
            else 0.25
        )
        oW = (
            0.3
            if platform_service.is_macos
            else 0.375
            if platform_service.is_windows
            else 0.25
        )

        rect = self._scale_rect(rect, oH, oW)
        if platform_service.is_macos:
            p.setPen(Qt.GlobalColor.transparent)
            p.setBrush(brush)
            top = QRect(rect)
            p.drawPolygon([top.topLeft(), top.bottomLeft(), top.topRight()])
            bottom = rect.adjusted(1, 1, 1, 1)
            p.drawPolygon(
                [bottom.topRight(), bottom.bottomLeft(), bottom.bottomRight()]
            )
        else:
            p.drawRoundedRect(rect, 1, 1)

    def _draw_min(self, p: QPainter, rect: QRect, color: QColor, action: Action):
        pen, brush = self._get_shape_tools(color, action)
        p.setPen(pen)

        oH = (
            0.3
            if platform_service.is_macos
            else 0.325
            if platform_service.is_windows
            else 0.25
        )
        oW = (
            0.3
            if platform_service.is_macos
            else 0.375
            if platform_service.is_windows
            else 0.25
        )

        rect = self._scale_rect(rect, oH, oW)
        div = 2 if platform_service.is_macos or platform_service.is_windows else 1
        half = rect.y() + (rect.height() / div)
        p.drawLine(QLine(rect.x(), half, rect.x() + rect.width(), half))

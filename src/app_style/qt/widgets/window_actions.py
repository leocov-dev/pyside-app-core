from enum import IntEnum
from typing import Callable, NamedTuple, Tuple

from PySide6.QtCore import QEvent, QLine, QPoint, QRect, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QResizeEvent,
)
from PySide6.QtWidgets import QWidget

from app_style.services.platform_service import PlatformService as PS
from app_style.generator_utils.style_types import QSSTheme


class Action(IntEnum):
    NONE = 0
    CLOSE = 1
    MINIMIZE = 2
    MAXIMIZE = 3


ShapeFunc = Callable[[QPainter, QRect, QColor, Action], None]


class ButtonData(NamedTuple):
    color: QColor
    action: Action
    signal: Signal
    shape_fn: ShapeFunc


class WindowActions(QWidget):
    close_clicked = Signal()
    minimize_clicked = Signal()
    maximize_clicked = Signal()

    def __init__(
        self,
        parent: QWidget,
        theme: QSSTheme,
    ):
        super(WindowActions, self).__init__(parent=parent)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setContentsMargins(10, 12, 0, 0)

        self._theme = theme
        self._hover = Action.NONE
        self._press = Action.NONE
        self._focus = True

        self._pen = QPen(Qt.GlobalColor.transparent)

        self._brush = QBrush(Qt.GlobalColor.transparent)

        _top_offset = self.contentsMargins().top() if PS.IsMacOS else 0
        self._side_offset = (
            self.contentsMargins().left()
            if PS.IsMacOS
            else self.contentsMargins().right()
        )
        if PS.IsMacOS:
            _width = 14
        elif PS.IsWindows:
            _width = 45
        else:
            _width = 20

        if PS.IsMacOS:
            _height = 14
        elif PS.IsWindows:
            _height = 35
        else:
            _height = 20

        _spacing = 3 if PS.IsWindows else 5 if PS.IsMacOS else 10

        self._a_rect = QRect(self._side_offset, _top_offset, _width, _height)
        self._b_rect = self._a_rect.translated(_width + _spacing, 0)
        self._c_rect = self._b_rect.translated(_width + _spacing, 0)

        self.container_height = (
            self._a_rect.y() + self._a_rect.height()
            if PS.IsWindows
            else self._a_rect.y() + self._a_rect.height() + self.contentsMargins().top()
            if PS.IsMacOS
            else self._a_rect.y()
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
                theme.win_minimize,
                Action.MINIMIZE,
                self.minimize_clicked,
                self._draw_min,
            ),
            ButtonData(
                theme.win_maximize,
                Action.MAXIMIZE,
                self.maximize_clicked,
                self._draw_max,
            ),
            ButtonData(
                theme.win_close, Action.CLOSE, self.close_clicked, self._draw_close
            ),
        ]

        _order = [2, 0, 1] if PS.IsMacOS else [0, 1, 2]
        self._rect_map = []
        for i, o in enumerate(_order):
            self._rect_map.append((_rect_list[i], _button_data[o]))

    def paintEvent(self, event: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.GlobalColor.transparent)
        p.setBrush(Qt.GlobalColor.transparent)

        for rect, data in self._rect_map:
            c_background = (
                data.color if self.isActiveWindow() else self._theme.win_action_inactive
            )
            self._draw_shape(p, rect, c_background, data.action)

            if PS.IsMacOS and not self.isActiveWindow():
                pass
            else:
                c_shape = (
                    data.color if self.isActiveWindow() else data.color.darker(300)
                )
                c_shape = c_shape.darker(200) if PS.IsMacOS else c_shape
                data.shape_fn(p, rect, c_shape, data.action)

        p.end()

        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        prev = self._hover
        for rect, data in self._rect_map:
            if rect.contains(event.pos()):
                self._hover = data.action
                break
        else:
            self._hover = Action.NONE

        if self._hover != prev:
            # repaint only on hover change
            self.update()

        super().mouseReleaseEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._hover = Action.NONE
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        for rect, data in self._rect_map:
            if rect.contains(event.pos()):
                data.signal.emit()
                break

        self._press = Action.NONE

        self.update()

        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        for rect, data in self._rect_map:
            if rect.contains(event.pos()):
                self._press = data.action
                break
        else:
            self._press = Action.NONE

        self.update()

        super().mousePressEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        if PS.IsMacOS:
            pass
        elif PS.IsWindows:
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

    def _get_shape_color(self, color: QColor) -> QColor:
        if PS.IsWindows:
            return QColor(Qt.GlobalColor.transparent)
        else:
            return color

    def _draw_shape(self, p: QPainter, rect: QRect, color: QColor, action: Action):
        p.setPen(Qt.GlobalColor.transparent)

        f_col = self._get_shape_color(color)

        if self._hover == action:
            f_col = color
        if self._press == action:
            f_col = color.lighter(135)

        p.setBrush(f_col)

        if PS.IsWindows:
            p.drawRect(rect)
        elif PS.IsMacOS:
            p.drawEllipse(rect)
        elif action == Action.CLOSE:
            p.drawEllipse(rect)

    def _get_shape_tools(self, color: QColor, action: Action) -> Tuple[QPen, QBrush]:
        if self._press == action:
            color = color if PS.IsMacOS else color.lighter(200)
        elif self._hover == action:
            color = (
                color
                if PS.IsMacOS
                else color.lighter()
                if PS.IsWindows
                else color.lighter(175)
            )
        else:
            color = (
                Qt.GlobalColor.transparent
                if PS.IsMacOS
                else color
                if PS.IsWindows
                else color.lighter()
            )

        pen = QPen(color)
        pen.setWidth(3 if PS.IsWindows else 2)
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

        oH = 0.3 if PS.IsMacOS else 0.325 if PS.IsWindows else 0.35
        oW = 0.3 if PS.IsMacOS else 0.375 if PS.IsWindows else 0.35

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

        oH = 0.3 if PS.IsMacOS else 0.325 if PS.IsWindows else 0.25
        oW = 0.3 if PS.IsMacOS else 0.375 if PS.IsWindows else 0.25

        rect = self._scale_rect(rect, oH, oW)
        if PS.IsMacOS:
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

        oH = 0.3 if PS.IsMacOS else 0.325 if PS.IsWindows else 0.25
        oW = 0.3 if PS.IsMacOS else 0.375 if PS.IsWindows else 0.25

        rect = self._scale_rect(rect, oH, oW)
        div = 2 if PS.IsMacOS or PS.IsWindows else 1
        half = rect.y() + (rect.height() / div)
        p.drawLine(QLine(rect.x(), half, rect.x() + rect.width(), half))


if __name__ == "__main__":
    p1 = QPoint(0, 0)
    print(p1)
    print(p1 - QPoint(2, 2))

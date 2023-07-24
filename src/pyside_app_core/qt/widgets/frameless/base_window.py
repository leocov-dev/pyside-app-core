from typing import Tuple

from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QResizeEvent,
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout

from pyside_app_core.qt.widgets.frameless.window_actions import WindowActions
from pyside_app_core.qt.widgets.frameless.window_shade import FramelessWindowShade
from pyside_app_core.services import application_service, platform_service


class FramelessBaseMixin:
    close_window = Signal()

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(FramelessBaseMixin, self).__init__(*args, **kwargs)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setMinimumSize(300, 128)

        self._theme = application_service.get_app_theme()

        self._top_layout = QVBoxLayout()
        self._top_layout.setContentsMargins(5, 0, 5, 5)
        self._title = QLabel("", parent=self)
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.MinimumExpanding,
        )
        self._title.setFixedHeight(32)
        self._top_layout.addWidget(
            self._title,
            alignment=Qt.AlignmentFlag.AlignTop,
        )

        self.setLayout(self._top_layout)

        self._moving = False
        self._screen_number: int = 0
        self._move_offset = QPoint(0, 0)
        self._move_corner = self.window().rect().bottomRight()
        self._can_minimize = True
        self._can_maximize = True

        self._window_actions = WindowActions(parent=self)
        self._window_actions.close_clicked.connect(self.close)
        self._window_actions.minimize_clicked.connect(self._on_minimize)
        self._window_actions.maximize_clicked.connect(self._on_maximize)

        self._window_shade = FramelessWindowShade(parent=self)

    @property
    def window_bar_rect(self) -> QRect:
        return QRect(
            0, 0, self.rect().width(), self._window_actions.geometry().height()
        )

    def setWindowTitle(self, title: str):
        self._title.setText(title)
        super().setWindowTitle(title)

    def layout(self) -> QVBoxLayout:
        return super().layout()

    def setFixedSize(self, *args):
        if not args:
            raise ValueError

        if len(args) == 1 and isinstance(args[0], QSize):
            super().setFixedSize(args[0])
            self._can_maximize = False
            return

        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            super().setFixedSize(args[0], args[1])
            self._can_maximize = False
            return

        raise ValueError

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(Qt.GlobalColor.transparent)
        p.setBrush(self._theme.background_color)

        p.drawRoundedRect(
            self.rect(), self._theme.win_corner_radius, self._theme.win_corner_radius
        )

        self._draw_border(p, self.rect())

        # TODO: a bit crude - we want the border to be on top of everything, but no need to call
        #  every time - how to call after all subclasses have added edited widgets? unknown...
        self._window_shade.raise_()
        self._window_actions.raise_()

        p.end()
        event.accept()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._title.setFixedWidth(self.rect().width())
        self._window_actions.resizeEvent(event)
        super().resizeEvent(event)

    def _draw_border(self, p: QPainter, rect: QRect):
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
        p.setClipping(False)

    def _on_maximize(self):
        if self.isMaximized():
            self.setWindowState(Qt.WindowState.WindowNoState)
        else:
            self.setWindowState(Qt.WindowState.WindowMaximized)

    def _on_minimize(self):
        self.setWindowState(Qt.WindowState.WindowMinimized)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._moving:
            win = self.window()
            pos = win.mapToGlobal(event.pos())
            target = pos - self._move_offset
            win.move(target)

            self.update()

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if (
            (event.buttons() & Qt.MouseButton.LeftButton) == Qt.MouseButton.LeftButton
            and self.window_bar_geo.contains(event.pos())
            and not self._window_actions.geometry().contains(event.pos())
        ):
            self._moving = True

            win = self.window()
            rect = win.rect()
            pos: QPoint = win.mapToGlobal(event.pos())
            corner: QPoint = win.mapToGlobal(rect.topLeft())
            self._move_offset = pos - corner
            self._move_corner = rect.bottomRight()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._moving = False
        self.update()

        super().mouseReleaseEvent(event)

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import (
    QBitmap,
    QBrush,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QResizeEvent,
)
from PySide6.QtWidgets import QMainWindow, QWidget

from app_style.qt.widgets.menu_ctx import MenuBarContext
from app_style.qt.widgets.tool_bar_ctx import ToolBarContext
from app_style.qt.widgets.window_actions import WindowActions
from app_style.qt.widgets.window_settings_mixin import WindowSettingsMixin
from app_style.services.platform_service import PlatformService
from app_style.generator_utils.style_types import QSSTheme


class FramelessWindow(WindowSettingsMixin, QMainWindow):
    def __init__(
        self,
        toolbar: bool,
        theme: QSSTheme,
    ):
        super(FramelessWindow, self).__init__(parent=None)

        self._theme = theme
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMouseTracking(True)

        self._corner_rounding = theme.win_corner_radius
        self._moving = False
        self._screen_number: int = 0
        self._move_offset = QPoint(0, 0)
        self._move_corner = self.window().rect().bottomRight()

        self._menu_bar = MenuBarContext(
            self,
            border_width=0 if PlatformService.IsMacOS else theme.win_divider_width,
            border_color=theme.win_divider_color,
        )

        self._menu_bar.setNativeMenuBar(PlatformService.IsMacOS)
        self.setMenuWidget(self._menu_bar)

        if toolbar:
            self._tool_bar = ToolBarContext(
                area="top", parent=self, theme=theme, movable=False
            )

        self._actions = WindowActions(parent=self, theme=theme)

        self._actions.close_clicked.connect(self.close)
        self._actions.minimize_clicked.connect(self._on_minimize)
        self._actions.maximize_clicked.connect(self._on_maximize)

        self._menu_bar.set_offset(
            5 if PlatformService.IsMacOS and toolbar else self._actions.container_height
        )
        self._menu_bar.set_shift(8)

        if PlatformService.IsMacOS and toolbar:
            self.setUnifiedTitleAndToolBarOnMac(True)
            spacer = QWidget(self)
            spacer.setFixedWidth(self._actions.container_width + 5)
            self._tool_bar.addWidget(spacer)

        self._window_border = FramelessWindowBorder(parent=self, theme=theme)

    @property
    def menu_bar(self):
        return self._menu_bar

    @property
    def tool_bar(self):
        return self._tool_bar

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        # TODO: a bit crude - we want the border to be on top of everything, but no need to call
        #  every time - how to call after all subclasses have added edited widgets? unknown...
        self._window_border.raise_()

        rect = self.rect()

        b = self._generate_bitmap_mask(rect)
        self.setMask(b)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._actions.resizeEvent(event)
        super().resizeEvent(event)

    def _generate_bitmap_mask(self, rect: QRect) -> QBitmap:
        b = QBitmap(rect.size())
        b.fill(Qt.GlobalColor.white)
        p = QPainter(b)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setBrush(Qt.GlobalColor.black)
        p.drawRoundedRect(rect, self._corner_rounding, self._corner_rounding)
        p.end()

        return b

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
            event.buttons() & Qt.MouseButton.LeftButton
        ) == Qt.MouseButton.LeftButton and self._menu_bar.rect().contains(event.pos()):
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


class FramelessWindowBorder(QWidget):
    def __init__(
        self,
        parent: QWidget,
        theme: QSSTheme,
    ):
        super(FramelessWindowBorder, self).__init__(parent=parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._corner_rounding = theme.win_corner_radius
        self._theme = theme

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = self.parent().contentsRect()
        self.setFixedSize(rect.size())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
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

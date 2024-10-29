from typing import cast

from PySide6.QtGui import QPainter, QPaintEvent, QPalette
from PySide6.QtWidgets import QGraphicsBlurEffect, QWidget


class BaseMixin:
    def __init__(
        self,
        *args: object,
        **kwargs: object,
    ):
        super().__init__(*args, **kwargs)

        cast(QWidget, self).setMouseTracking(True)
        cast(QWidget, self).setMinimumSize(256, 128)


class Shade(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setHidden(True)

    def gfx(self) -> QGraphicsBlurEffect:
        gfx = QGraphicsBlurEffect(self)
        gfx.setBlurHints(QGraphicsBlurEffect.BlurHint.QualityHint)
        gfx.setBlurRadius(0)
        return gfx

    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)

        color = self.palette().color(QPalette.ColorRole.Window)
        color.setAlpha(175)
        painter.fillRect(self.rect(), color)

        painter.end()

    def update_size(self) -> None:
        self.setGeometry(self.window().rect())

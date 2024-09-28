from PySide6.QtCore import Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from pyside_app_core.services.preferences_service import PrefGroup, PrefSection


class _Link(QLabel):
    clicked = Signal(object)

    def __init__(
        self,
        item: PrefSection | PrefGroup,
        parent: QWidget | None = None,
    ):
        super().__init__(item.display_name, parent)

        self._item = item

        self.setStyleSheet(
            f"""
            QLabel {{
                color: {self.palette().accent().color().name()};
                text-decoration: underline;
            }}
            QLabel:pressed{{
                color: {self.palette().accent().color().darker().name()};
            }}
            QLabel:hover{{
                color: {self.palette().accent().color().lighter().name()};
            }}
            """
        )

    def mouseReleaseEvent(self, _: QMouseEvent) -> None:
        self.clicked.emit(self._item)


class SectionListPage(QWidget):
    navigate = Signal(object)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        _ly = QVBoxLayout()
        self.setLayout(_ly)

        self._heading = QLabel("", self)
        font = self._heading.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSizeF() * 1.25)
        self._heading.setFont(font)
        _ly.addWidget(self._heading)

        _ly.addSpacing(20)

        self._links = QVBoxLayout()
        self._links.setContentsMargins(15, 0,0,0)
        _ly.addLayout(self._links)

    def set_section(self, section: PrefSection) -> None:
        self._clear()

        self._heading.setText(section.display_name)

        for item in section:
            link = _Link(item, self)
            link.clicked.connect(self.navigate.emit)

            self._links.addWidget(link)

        self._links.addStretch(99)

    def _clear(self) -> None:
        while child := self._links.takeAt(0):
            if w := child.widget():
                w.deleteLater()
            del child

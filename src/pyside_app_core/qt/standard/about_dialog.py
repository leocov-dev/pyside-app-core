from typing import cast

from jinja2 import BaseLoader, Environment
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from pyside_app_core.qt.application_service import AppMetadata, TemplateMeta
from pyside_app_core.utils.files import load_text_file


class AboutDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(640, 480)
        self.setWindowTitle(f"About {AppMetadata.name}")

        _ly = QVBoxLayout()
        _ly.setContentsMargins(0, 0, 0, 10)
        _ly.setSpacing(5)
        self.setLayout(_ly)

        _tabs = QTabWidget(parent=self)
        _ly.addWidget(_tabs)

        _tabs.addTab(_AboutApp(parent=self), "About")
        _tabs.addTab(_Licenses(parent=self), "Licenses")

        _ly_btns = QHBoxLayout()
        _ly_btns.setContentsMargins(10, 0, 10, 0)
        _close = QPushButton("Close", self)
        _close.setDefault(True)
        _ly_btns.addWidget(_close, alignment=Qt.AlignmentFlag.AlignRight)
        _ly.addLayout(_ly_btns)

        _close.clicked.connect(self.close)


class _AboutApp(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        _ly_split = QHBoxLayout()
        _ly_split.setContentsMargins(15, 1, 1, 2)
        _ly_split.setSpacing(10)
        self.setLayout(_ly_split)

        _ly_icon = QVBoxLayout()
        _ly_icon.setContentsMargins(0, 10, 0, 0)
        icon = QLabel(parent=self)
        icon.setPixmap(cast(QApplication, QApplication.instance()).windowIcon().pixmap(64, 64))
        _ly_icon.addWidget(icon, stretch=1, alignment=Qt.AlignmentFlag.AlignTop)
        _ly_split.addLayout(_ly_icon)

        text_area = QTextBrowser()
        text_area.setViewportMargins(10, 10, 10, 10)
        text_area.setStyleSheet(
            f"""
        QTextBrowser {{
            background-color: {self.palette().color(QPalette.ColorRole.Window).name()};
            border: none;
        }}
        """
        )
        _ly_split.addWidget(text_area, stretch=99)

        args: dict[str, str] = {
            "name": AppMetadata.name,
            "version": AppMetadata.version,
            "id": AppMetadata.id,
        }

        env = Environment(loader=BaseLoader(), autoescape=True)
        if template_data := AppMetadata.about_template:
            raw, data = cast(TemplateMeta, template_data)
            args = {**args, **(data or {})}
        else:
            raw = load_text_file(":/core/notices/about.md.jinja2")

        template = env.from_string(raw)

        text_area.setMarkdown(template.render(**args))


class _Licenses(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        _ly = QVBoxLayout()
        _ly.setContentsMargins(1, 1, 1, 1)
        self.setLayout(_ly)

        text_area = QTextBrowser()
        text_area.setViewportMargins(10, 10, 10, 10)
        text_area.setStyleSheet(
            f"""
        QTextBrowser {{
            background-color: {self.palette().color(QPalette.ColorRole.Window).name()};
            border: none;
        }}
        """
        )
        _ly.addWidget(text_area, stretch=99)

        markdown = """
# Open Source Licenses
"""
        for lic in AppMetadata.oss_licenses:
            markdown = f"""{markdown}

---

{load_text_file(lic)}"""

        text_area.setMarkdown(markdown)

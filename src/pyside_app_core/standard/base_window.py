from typing import cast

from PySide6.QtWidgets import QWidget

from pyside_app_core.qt import application_service


class BaseMixin:
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super(BaseMixin, self).__init__(*args, **kwargs)

        cast(QWidget, self).setMouseTracking(True)
        cast(QWidget, self).setMinimumSize(300, 128)

        self._theme = application_service.get_app_theme()

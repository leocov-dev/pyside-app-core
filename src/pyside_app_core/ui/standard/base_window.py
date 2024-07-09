from typing import cast

from PySide6.QtWidgets import QWidget


class BaseMixin:
    def __init__(
        self,
        *args: object,
        **kwargs: object,
    ):
        super().__init__(*args, **kwargs)

        cast(QWidget, self).setMouseTracking(True)
        cast(QWidget, self).setMinimumSize(256, 128)

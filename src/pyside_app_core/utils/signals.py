from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, SignalInstance

from pyside_app_core import log

_SignalCallback = Callable[..., None]


class OneToManySwitcher(QObject):
    """
    when a signal is connected to many consumers we can selectively forward
    events only to one specific consumer at a time
    """

    def __init__(self, signal: SignalInstance, parent: QObject):
        super().__init__(parent=parent)

        self._consumer_index = -1
        self._consumers: list[_SignalCallback] = []

        # ----
        signal.connect(self._interposer)

    def _interposer(self, *args: Any) -> None:
        if self._consumer_index < 0:
            log.debug(f"{self.__class__.__name__} does not have any connected consumers")
            return

        self._consumers[self._consumer_index](*args)

    def connect_switched(self, consumer_cb: _SignalCallback) -> int:
        self._consumers.append(consumer_cb)

        if self._consumer_index < 0:
            self._consumer_index = 0

        return len(self._consumers) - 1

    def set_current_index(self, index: int) -> None:
        if len(self._consumers) < index + 1:
            raise IndexError(f"no switched consumer registered at inded: {index}")

        self._consumer_index = index

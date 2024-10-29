import contextlib
from collections.abc import Generator

from PySide6.QtGui import QPainter

from pyside_app_core import log


@contextlib.contextmanager
def safe_paint(painter: QPainter) -> Generator[QPainter, None, None]:
    painter.save()

    try:
        yield painter
    except Exception as e:  # noqa: BLE001
        log.warning(f"paining error: {e}")
    finally:
        painter.restore()

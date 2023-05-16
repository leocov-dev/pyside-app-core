from dataclasses import dataclass
from pathlib import Path
from typing import List

from pyside_app_core.qt.util.pixel_val import PixelVal
from pyside_app_core.qt.util.s_color import SColor
from pyside_app_core.services import platform_service


@dataclass(frozen=True)
class QtResourceFile:
    path: str | Path
    alias: str | None = None


@dataclass(frozen=True)
class QtResourceGroup:
    files: List[QtResourceFile]
    prefix: str | None = None
    lang: str | None = None


class QssTheme:
    background_color = SColor(60)
    background_color_inactive = SColor(70)

    text_color = SColor(250)
    text_color_inactive = SColor(200)
    text_color_disabled = SColor(120)

    win_corner_radius = PixelVal(12)
    widget_corner_radius = PixelVal(8)

    win_divider_width = PixelVal(2)
    win_divider_color = SColor(85)

    widget_accent_main_color = SColor(80, 160, 250)
    widget_accent_neutral_color = SColor(85)
    widget_border_color = SColor(95)
    widget_hover_color = SColor(95)

    input_background_color = SColor(95)
    input_background_color_inactive = SColor(85)

    tooltip_background_color = SColor(85)

    win_close = SColor(120) if platform_service.is_windows else SColor(237, 107, 95)
    win_minimize = SColor(120) if platform_service.is_windows else SColor(245, 191, 79)
    win_maximize = SColor(120) if platform_service.is_windows else SColor(98, 197, 84)
    win_action_inactive = SColor(85)


DEFAULT_THEME = QssTheme()

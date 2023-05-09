from typing import Self

from PySide6.QtGui import QColor


class SColor(QColor):
    def __init__(self, *args, **kwargs):
        if (
            len(args) == 1
            and not kwargs
            and (isinstance(args[0], int) or isinstance(args[0], float))
        ):
            val = args[0]
            super(SColor, self).__init__(val, val, val)
        else:
            super(SColor, self).__init__(*args, **kwargs)

    def lighter(self, f=150) -> Self:
        return self.__class__(super().lighter(f))

    def darker(self, f=150) -> Self:
        return self.__class__(super().darker(f))

    def desaturated(self, f=150) -> Self:
        hsv = self.toHsv()
        hsv.setHsv(
            hsv.hue(),
            min(max(hsv.saturation() * (2 - max(f, 0) / 100.0), 0), 255),
            hsv.value(),
        )
        return self.__class__(hsv.toRgb())

    def __str__(self):
        return f"rgb({self.red()},{self.green()},{self.blue()})"

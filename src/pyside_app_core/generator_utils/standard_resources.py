from pathlib import Path
from typing import List

from pyside_app_core.generator_utils.style_types import QtResourceFile, QtResourceGroup

__root = Path(__file__).parent

STANDARD_RESOURCES: List[QtResourceGroup] = [
    QtResourceGroup(files=[QtResourceFile("style.qss")]),
    QtResourceGroup(
        prefix="std/",
        files=[
            QtResourceFile(
                str(__root / "icons" / "console.svg"), alias="icons/console"
            ),
            QtResourceFile(
                str(__root / "icons" / "down-arrow.svg"), alias="icons/down-arrow"
            ),
            QtResourceFile(
                str(__root / "icons" / "grab-corner.svg"), alias="icons/grab-corner"
            ),
            QtResourceFile(str(__root / "icons" / "reload.svg"), alias="icons/reload"),
            QtResourceFile(str(__root / "icons" / "save.svg"), alias="icons/save"),
            QtResourceFile(
                str(__root / "icons" / "spin-down/normal.svg"),
                alias="icons/spin-down/normal",
            ),
            QtResourceFile(
                str(__root / "icons" / "spin-down/disabled.svg"),
                alias="icons/spin-down/disabled",
            ),
            QtResourceFile(
                str(__root / "icons" / "spin-up/normal.svg"),
                alias="icons/spin-up/normal",
            ),
            QtResourceFile(
                str(__root / "icons" / "spin-up/disabled.svg"),
                alias="icons/spin-up/disabled",
            ),
        ],
    ),
]

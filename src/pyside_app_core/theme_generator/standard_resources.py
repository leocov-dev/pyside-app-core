from pathlib import Path
from typing import List

from pyside_app_core.theme_generator.style_types import QtResourceFile, QtResourceGroup

__resources = Path(__file__).parent.parent / "resources"


STANDARD_RESOURCES: List[QtResourceGroup] = [
    QtResourceGroup(files=[QtResourceFile("style.qss")]),  # type: ignore[call-arg]
    QtResourceGroup(  # type: ignore[call-arg]
        prefix="std/",
        files=[
            QtResourceFile(
                str(__resources / "icons" / "console.svg"), alias="icons/console"
            ),
            QtResourceFile(
                str(__resources / "icons" / "down-arrow.svg"), alias="icons/down-arrow"
            ),
            QtResourceFile(
                str(__resources / "icons" / "grab-corner.svg"),
                alias="icons/grab-corner",
            ),
            QtResourceFile(
                str(__resources / "icons" / "reload.svg"), alias="icons/reload"
            ),
            QtResourceFile(str(__resources / "icons" / "save.svg"), alias="icons/save"),
            QtResourceFile(
                str(__resources / "icons" / "spin-down/normal.svg"),
                alias="icons/spin-down/normal",
            ),
            QtResourceFile(
                str(__resources / "icons" / "spin-down/disabled.svg"),
                alias="icons/spin-down/disabled",
            ),
            QtResourceFile(
                str(__resources / "icons" / "spin-up/normal.svg"),
                alias="icons/spin-up/normal",
            ),
            QtResourceFile(
                str(__resources / "icons" / "spin-up/disabled.svg"),
                alias="icons/spin-up/disabled",
            ),
        ],
    ),
]

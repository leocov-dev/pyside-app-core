from typing import List

from pyside_app_core.generator_utils.style_types import QtResourceFile, QtResourceGroup

STANDARD_RESOURCES: List[QtResourceGroup] = [
    QtResourceGroup(files=[QtResourceFile("style.qss")]),
    QtResourceGroup(
        prefix="std/",
        files=[
            QtResourceFile("icons/console.svg", alias="icons/console"),
            QtResourceFile("icons/down-arrow.svg", alias="icons/down-arrow"),
            QtResourceFile("icons/grab-corner.svg", alias="icons/grab-corner"),
            QtResourceFile("icons/reload.svg", alias="icons/reload"),
            QtResourceFile("icons/save.svg", alias="icons/save"),
            QtResourceFile(
                "icons/spin-down/normal.svg", alias="icons/spin-down/normal"
            ),
            QtResourceFile(
                "icons/spin-down/disabled.svg", alias="icons/spin-down/disabled"
            ),
            QtResourceFile("icons/spin-up/normal.svg", alias="icons/spin-up/normal"),
            QtResourceFile(
                "icons/spin-up/disabled.svg", alias="icons/spin-up/disabled"
            ),
        ],
    ),
]

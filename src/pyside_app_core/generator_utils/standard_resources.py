from typing import List

from pyside_app_core.generator_utils.style_types import QtResourceFile, QtResourceGroup

STANDARD_RESOURCES: List[QtResourceGroup] = [
    QtResourceGroup(files=[QtResourceFile("style.qss")]),
    QtResourceGroup(
        prefix="std/",
        files=[
            QtResourceFile("icons/console.svg", alias="icons/console"),
            QtResourceFile("icons/down-arrow.svg"),
            QtResourceFile("icons/grab-corner.svg"),
            QtResourceFile("icons/reload.svg"),
            QtResourceFile("icons/save.svg"),
            QtResourceFile("icons/spin-down.svg"),
            QtResourceFile("icons/spin-down-disabled.svg"),
            QtResourceFile("icons/spin-up.svg"),
            QtResourceFile("icons/spin-up-disabled.svg"),
        ],
    ),
]

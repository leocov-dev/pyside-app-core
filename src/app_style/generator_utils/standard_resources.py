from typing import List

from app_style.generator_utils.style_types import QtResourceFile, QtResourceGroup

STANDARD_RESOURCES: List[QtResourceGroup] = [
    QtResourceGroup(files=[QtResourceFile("style.qss")]),
    QtResourceGroup(
        prefix="std/",
        files=[
            QtResourceFile("icons/console.svg"),
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

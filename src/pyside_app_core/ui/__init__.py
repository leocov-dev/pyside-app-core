import pprint
import sys
from pathlib import Path

from PySide6.QtCore import QResource

from pyside_app_core import log


def assert_resources_file(rcc: Path | None) -> Path:
    """if the given rcc file is None or not found then will try to get a 'default' resource file"""
    if rcc and rcc.exists():
        return rcc

    from pyside_app_core.services import debug_service

    tried = []

    for i in range(10):
        try:
            caller = debug_service.get_caller_file(2, i)
            rcc = caller.parent / "resources.rcc"
            tried.append(str(rcc))
            if rcc.exists():
                break
        except IndexError:
            # ignore caller frame depth index errors
            pass
    else:
        log.error(
            f"No resource.rcc file given or found, attempted:\n"
            f'{pprint.pformat([t for t in sorted(set(tried)) if "/" in t], compact=False)}\n'
            f"Will now exit.",
            file=sys.stderr,
        )
        sys.exit(1)

    return rcc


def register_resource_file(rcc: Path | None) -> None:
    # registering a binary rcc is marginally faster than importing a python resource module
    QResource.registerResource(str(assert_resources_file(rcc)))

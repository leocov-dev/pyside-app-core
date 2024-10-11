import pprint
import sys
from pathlib import Path

from PySide6.QtCore import QResource

from pyside_app_core import log
from pyside_app_core.errors.basic_errors import ApplicationError


def assert_resources_file(rcc: Path | None) -> Path:
    """if the given rcc file is None or not found then will try to get a 'default' resource file"""
    if rcc and rcc.exists():
        return rcc

    from pyside_app_core.services import debug_service

    tried = []

    for i in range(10, -1, -1):
        try:
            caller = debug_service.get_caller_file(i)
            rcc = caller.parent / "resources.rcc"
            tried.append(str(rcc))
            if rcc.exists():
                break
        except IndexError:
            # ignore caller frame depth index errors
            pass
        except StopIteration:
            # raised in standalone Nuitka build
            break

    tried_pp = pprint.pformat([t for t in sorted(set(tried)) if "/" in t], compact=False)

    log.debug(f"searched for resource.rcc in:\n{tried_pp}")
    if rcc and rcc.exists():
        return rcc

    raise ApplicationError(
        f"No resource.rcc file given or found, attempted:\n"
        f'{tried_pp}\n'
        f"Will now exit.",
    )


def register_resource_file(rcc: Path | None) -> None:
    # registering a binary rcc is marginally faster than importing a python resource module
    QResource.registerResource(str(assert_resources_file(rcc)))

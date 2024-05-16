import os
import platform

__valid_platforms = ["Darwin", "Windows", "Linux"]
__platform: str | None = None


def _platform() -> str:
    global __platform

    system_platform = platform.system()
    override = os.environ.get("PLATFORM_OVERRIDE", system_platform)

    if not __platform:
        __platform = override if override in __valid_platforms else system_platform

    return __platform


is_macos = _platform() == "Darwin"
is_windows = _platform() == "Windows"
is_linux = _platform() == "Linux"

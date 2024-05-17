import os
import platform

__valid_platforms = ["Darwin", "Windows", "Linux"]


def _platform() -> str:
    system_platform = platform.system()
    override = os.environ.get("PLATFORM_OVERRIDE", system_platform)

    return override if override in __valid_platforms else system_platform


__platform: str = _platform()

is_macos = __platform == "Darwin"
is_windows = __platform == "Windows"
is_linux = __platform == "Linux"

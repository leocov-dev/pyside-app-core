import platform


class PlatformService:
    IsMacOS = platform.system() == "Darwin"
    IsWindows = platform.system() == "Windows"

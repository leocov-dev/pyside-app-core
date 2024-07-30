class CoreError(Exception):
    """base error for application"""

    @property
    def internal(self) -> bool:
        return self._internal

    def __init__(self, msg: str, *, internal: bool = False):
        self._internal = internal
        super().__init__(msg)


class ApplicationError(CoreError):
    """something bad happened at the application level"""


class PreferencesError(CoreError):
    """something bad happened with managing preferences"""

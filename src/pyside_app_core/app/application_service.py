from pathlib import Path
from typing import NamedTuple

from PySide6.QtCore import QStandardPaths

from pyside_app_core.errors.basic_errors import ApplicationError

# def _Field(nullable: bool = False) -> Any:
#     class _FieldInfo:
#
#         _nullable = nullable
#
#         def __init__(self) -> None:
#             self.value: Any | None = None
#
#         def __set_name__(self, owner: type, name: str) -> None:
#             owner._fields.append(name)  # type: ignore[attr-defined]
#
#         def __get__(self, obj: object, objtype: type) -> Any:
#             print(f"fetching: {obj}, {objtype}")
#             if self.value is None and not self._nullable:
#                 raise ValueError("Field is not initialized")
#             return self.value
#
#         def __set__(self, obj: object, value: Any) -> None:
#             print(f"setting: {obj}, {value}")
#             self.value = value
#
#     return _FieldInfo


# class _NullableField(_Field[_FVT | None]):
#     def __get__(self, obj: object, objtype: type) -> _FVT | None:
#         return self.value
#
#     def __set__(self, obj: object, value: _FVT | None) -> None:
#         self.value = value


# class _MetadataMeta(type):
#     _initialized = False
#     _fields: ClassVar[list[str]] = []
#
#     def __str__(cls) -> str:
#         if not cls._initialized:
#             raise ApplicationError("AppMetadata not initialized")
#
#         vals: list[str] = []
#
#         for f in cls._fields:
#             val = cls.__dict__.get(f)
#             vals.append(f"{f}: {val}")
#
#         return f"<{cls.__name__}: [{', '.join(vals)}]>"


class _TemplateMeta(NamedTuple):
    resource: str
    data: dict[str, str] | None = None


class AppMetadata:
    id: str
    name: str
    version: str
    icon: str
    about_template: _TemplateMeta | None = None
    help_url: str
    bug_report_url: str
    oss_licenses: list[str]
    documents_dir: Path

    _initialized = False

    @classmethod
    def init(
        cls,
        app_id: str,
        name: str,
        version: str,
        icon_resource: str = "",
        about_template: _TemplateMeta | None = None,
        help_url: str = "",
        bug_report_url: str = "",
        oss_licenses: list[str] | None = None,
    ) -> None:
        if cls._initialized:
            raise ApplicationError("Metadata already initialized")

        cls.id = app_id
        cls.name = name
        cls.version = version
        cls.icon = icon_resource
        cls.about_template = about_template
        cls.help_url = help_url
        cls.bug_report_url = bug_report_url
        cls.oss_licenses = [
            # TODO: scan resources at runtime
            ":/core/notices/licenses/python.md",
            ":/core/notices/licenses/qt.md",
            ":/core/notices/licenses/jinja2.md",
            ":/core/notices/licenses/iconoir.md",
            ":/core/notices/licenses/loguru.md",
            *(oss_licenses or []),
        ]
        cls.documents_dir = (
            Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)) / name
        )

        cls._initialized = True

from typing import ClassVar, Generic, NamedTuple, TypeVar

from pyside_app_core.errors.basic_errors import ApplicationError

_FVT = TypeVar("_FVT")


class Field(Generic[_FVT]):
    def __init__(self, _: type[_FVT]) -> None:
        self.value: _FVT | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        owner._fields.append(name)  # type: ignore[attr-defined]

    def __get__(self, obj: object, objtype: type) -> _FVT:
        if self.value is None:
            raise ValueError("Field is not initialized")
        return self.value

    def __set__(self, obj: object, value: _FVT) -> None:
        self.value = value


class NullableField(Field[_FVT | None]):
    def __get__(self, obj: object, objtype: type) -> _FVT | None:
        return self.value

    def __set__(self, obj: object, value: _FVT | None) -> None:
        self.value = value


class MetadataMeta(type):
    _initialized = False
    _fields: ClassVar[list[str]] = []

    def __str__(cls) -> str:
        if not cls._initialized:
            raise ApplicationError("Meta not initialized")

        vals: list[str] = []

        for f in cls._fields:
            val = cls.__dict__.get(f)
            vals.append(f"{f}: {val}")

        return f"<{cls.__name__}: [{', '.join(vals)}]>"


class TemplateMeta(NamedTuple):
    resource: str
    data: dict[str, str] | None = None


class AppMetadata(metaclass=MetadataMeta):
    id = Field(str)
    name = Field(str)
    version = Field(str)
    icon = Field(str)
    about_template = NullableField(TemplateMeta)
    help_url = Field(str)
    bug_report_url = Field(str)
    oss_licenses = Field(list)

    @classmethod
    def init(
        cls,
        app_id: str,
        name: str,
        version: str,
        icon_resource: str = "",
        about_template: TemplateMeta | None = None,
        help_url: str = "",
        bug_report_url: str = "",
        oss_licenses: list[str] | None = None,
    ) -> None:
        if cls._initialized:
            raise ApplicationError("Metadata already initialized")

        cls.id = app_id  # type: ignore[assignment]
        cls.name = name  # type: ignore[assignment]
        cls.version = version  # type: ignore[assignment]
        cls.icon = icon_resource  # type: ignore[assignment]
        cls.about_template = about_template  # type: ignore[assignment]
        cls.help_url = help_url  # type: ignore[assignment]
        cls.bug_report_url = bug_report_url  # type: ignore[assignment]
        cls.oss_licenses = [  # type: ignore[assignment]
            ":/core/notices/licenses/python.md",
            ":/core/notices/licenses/qt.md",
            ":/core/notices/licenses/jinja2.md",
            ":/core/notices/licenses/iconoir.md",
            *(oss_licenses or []),
        ]

        cls._initialized = True

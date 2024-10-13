import sys
from configparser import ConfigParser
from pathlib import Path

from typing_extensions import TypedDict


class _SpecApp(TypedDict):
    title: str
    project_dir: str
    input_file: str
    exec_directory: str
    project_file: str | None
    icon: str


class _SpecPython(TypedDict):
    python_path: str
    packages: str


class _SpecQt(TypedDict):
    qml_files: str | None
    excluded_qml_plugins: str | None
    modules: str
    plugins: str


_SpecNuitka = TypedDict(
    "_SpecNuitka",
    {
        "macos.permissions": str,
        "extra_args": str,
    },
)


class PySideSpec(TypedDict):
    app: _SpecApp
    python: _SpecPython
    qt: _SpecQt
    nuitka: _SpecNuitka


def build_deploy_spec(
    target_dir: Path,
    *,
    entrypoint: str,
    icon: Path,
    extra_python_packages: list[str] | None = None,
    extra_qt_modules: list[str] | None = None,
    extra_qt_plugins: list[str] | None = None,
    macos_permissions: list[str] | None = None,
    extra_package_data: list[str] | None = None,
    extra_data_dirs: list[str] | None = None,
) -> Path:
    python_packages = [
        "Nuitka",
        "ordered-set",
        "zstandard",
        "imageio",
        *(extra_python_packages or []),
    ]

    qt_modules = [
        "Widgets",
        "Core",
        "Gui",
        *(extra_qt_modules or []),
    ]

    qt_plugins = [
        "platforms/darwin",
        "platformthemes",
        "accessiblebridge",
        "platforms",
        "xcbglintegrations",
        "iconengines",
        "egldeviceintegrations",
        "platforminputcontexts",
        "imageformats",
        "generic",
        "styles",
        *(extra_qt_plugins or []),
    ]

    extra_args = [
        "--quiet",
        "--assume-yes-for-downloads",
        "--noinclude-qt-translations",
        "--static-libpython=no",
        "--report=compilation-report.xml",
        *[f"--include-package-data={d}" for d in (extra_package_data or [])],
        *[f"--include-data-dir={d}" for d in (extra_data_dirs or [])],
    ]

    data: PySideSpec = {
        "app": {
            "title": entrypoint.removesuffix(".py"),
            "project_dir": ".",
            "input_file": entrypoint,
            "exec_directory": ".",
            "project_file": "",
            "icon": str(icon),
        },
        "python": {
            "python_path": sys.executable,
            "packages": ",".join(sorted(set(python_packages))),
        },
        "qt": {
            "qml_files": "",
            "excluded_qml_plugins": "",
            "modules": ",".join(sorted(set(qt_modules or []))),
            "plugins": ",".join(sorted(set(qt_plugins or []))),
        },
        "nuitka": {
            "macos.permissions": ",".join(sorted(set(macos_permissions or []))),
            "extra_args": " ".join(sorted(set(extra_args or []))),
        },
    }

    parser = ConfigParser()
    parser.read_dict(data)  # type: ignore[arg-type]

    spec_target = target_dir / "_pysidedeploy.spec"

    with open(spec_target, "w") as f:
        parser.write(f)

    return spec_target


if __name__ == "__main__":
    build_deploy_spec(
        target_dir=Path(__file__).parent,
        entrypoint="ODC Commander.py",
        icon=Path("/Users/leo/src/odc-commander/src/resources/odc/app/icon.png"),
        extra_python_packages=[],
        extra_qt_modules=[
            "SerialPort",
            "DBus",
        ],
        extra_qt_plugins=[],
        macos_permissions=[],
        extra_package_data=["odc_commander"],
        extra_data_dirs=["./odc_firmware=odc_firmware"],
    )

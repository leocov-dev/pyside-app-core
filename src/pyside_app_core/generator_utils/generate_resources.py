import subprocess
from pathlib import Path
from typing import List, Literal, Type

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from pyside_app_core.generator_utils.standard_resources import STANDARD_RESOURCES
from pyside_app_core.generator_utils.style_types import QtResourceGroup
from pyside_app_core.qt.style import DEFAULT_THEME, QssTheme


def _compose_template_environment(*extra_template_files: Path) -> Environment:
    loaders = [PackageLoader("pyside_app_core.generator_utils")]

    if extra_template_files:
        dirs = list(set([str(p.parent) for p in extra_template_files]))
        loaders.append(FileSystemLoader(dirs))

    return Environment(loader=ChoiceLoader(loaders), autoescape=False)


def _compile_qss_template(theme: QssTheme, qss_extra: List[Path] | None = None) -> str:
    qss_extra = qss_extra or []
    env = _compose_template_environment(*qss_extra)
    qss_template = env.get_template("style.qss.jinja2")
    return qss_template.render(theme=theme, qss_extra=[q.name for q in qss_extra])


def _compile_qrc_template(resources: List[QtResourceGroup]) -> str:
    env = _compose_template_environment()
    qrc_template = env.get_template("resources.qrc.jinja2")
    return qrc_template.render(qresources=resources)


def _write_qss_file(data: str) -> Path:
    target = Path(__file__).parent / "style.qss"
    with open(target, "w") as f:
        f.write(data)

    return target


def _write_qrc_file(data: str) -> Path:
    target = Path(__file__).parent / "resources.qrc"
    with open(target, "w") as f:
        f.write(data)

    return target


ResourceFormat = Literal["python", "binary"]


def compile_qrc_to_resources(
    target_dir: Path,
    qss_theme: QssTheme | Type[QssTheme],
    rcc_format: ResourceFormat = "binary",
    qss_template_extra: List[Path] | None = None,
    resources_extra: List[QtResourceGroup] | None = None,
) -> Path:
    if not isinstance(qss_theme, QssTheme):
        qss_theme = qss_theme()

    _write_qss_file(
        _compile_qss_template(qss_theme or DEFAULT_THEME, qss_template_extra)
    )

    resources = STANDARD_RESOURCES
    if resources_extra:
        resources.extend(resources_extra)

    qrc_file = _write_qrc_file(_compile_qrc_template(resources))

    file_name = "resources.py"

    rcc_args = []
    if rcc_format == "binary":
        file_name = "resources.rcc"
        rcc_args.append("--binary")

    file_target = target_dir / file_name

    subprocess.check_call(
        ["pyside6-rcc", *rcc_args, "-o", str(file_target), str(qrc_file)]
    )

    return file_target

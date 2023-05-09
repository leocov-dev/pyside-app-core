import subprocess
from pathlib import Path
from typing import List, Literal

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from app_style.generator_utils.standard_resources import STANDARD_RESOURCES
from app_style.generator_utils.style_types import QSSTheme, QtResourceGroup


def _compose_template_environment(*extra_template_files: Path) -> Environment:
    loaders = [PackageLoader("core_style")]

    if extra_template_files:
        dirs = list(set([str(p.parent) for p in extra_template_files]))
        loaders.append(FileSystemLoader(dirs))

    return Environment(loader=ChoiceLoader(loaders), autoescape=False)


def _compile_qss_template(theme: QSSTheme, qss_extra: List[Path] | None = None) -> str:
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
    qss_theme: QSSTheme | None,
    rcc_format: ResourceFormat = "python",
    qss_template_extra: List[Path] | None = None,
    resources_extra: List[QtResourceGroup] | None = None,
) -> None:
    _write_qss_file(_compile_qss_template(qss_theme, qss_template_extra))

    resources = STANDARD_RESOURCES
    if resources_extra:
        resources.extend(resources_extra)

    qrc_file = _write_qrc_file(_compile_qrc_template(resources))

    file_name = "resources.py"

    rcc_args = []
    if rcc_format == "binary":
        file_name = "resources.rcc"
        rcc_args.append("--binary")

    subprocess.check_call(
        ["pyside6-rcc", *rcc_args, "-o", str(target_dir / file_name), str(qrc_file)]
    )

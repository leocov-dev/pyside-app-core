import subprocess
import tempfile
from pathlib import Path
from typing import Literal

from jinja2 import Environment, PackageLoader

from pyside_app_core.resource_generator.resource_types import (
    QtResourceFile,
    QtResourceGroup,
)

_std_resource_root = Path(__file__).parent.parent / "resources" / "core"


def _compile_qrc_template(resources: list[QtResourceGroup]) -> str:
    env = Environment(loader=PackageLoader("pyside_app_core.resources"), autoescape=True)
    qrc_template = env.get_template("resources.qrc.jinja2")
    return qrc_template.render(qresources=resources)


def _write_file(target: Path, data: str) -> Path:
    with open(target, "w") as f:
        f.write(data)

    return target


ResourceFormat = Literal["python", "binary"]


def _build_resource_groups(root_paths: list[Path]) -> list[QtResourceGroup]:
    groups: list[QtResourceGroup] = []
    root_prefixes: list[str] = []

    for root_path in root_paths:
        if not root_path.is_dir():
            continue

        prefix = root_path.name
        if prefix in root_prefixes:
            raise ValueError(f"Root path {root_path} has duplicate prefix {prefix}")

        root_prefixes.append(prefix)

        files: list[QtResourceFile] = []

        for item in root_path.glob("**/*"):
            if item.is_dir():
                continue
            files.append(
                QtResourceFile(
                    str(item),
                    item.relative_to(root_path).as_posix(),
                )
            )

        groups.append(
            QtResourceGroup(
                prefix,
                None,
                files,
            )
        )

    return groups


def compile_qrc_to_resources(
    target_dir: Path,
    rcc_format: ResourceFormat = "binary",
    additional_resource_roots: list[Path] | None = None,
    *,
    debug: bool = False,
) -> Path:
    with tempfile.TemporaryDirectory() as tempdir:
        temp_path = Path(tempdir)

        resources = _build_resource_groups(
            [
                _std_resource_root,
                *(additional_resource_roots or []),
            ]
        )

        qrc_file = _write_file(temp_path / "resources.qrc", _compile_qrc_template(resources))

        rcc_args = []

        if rcc_format == "binary":
            file_name = "resources.rcc"
            rcc_args.append("--binary")
        else:
            file_name = "resources.py"

        file_target = target_dir / file_name

        subprocess.check_call(["pyside6-rcc", *rcc_args, "-o", str(file_target), str(qrc_file)])

        if debug:
            print("-" * 80)
            print(qrc_file.read_text())
            print("-" * 80)

    return file_target

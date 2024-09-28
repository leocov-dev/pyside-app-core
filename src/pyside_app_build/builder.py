import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from hatchling.builders.config import BuilderConfig
from hatchling.builders.plugin.interface import BuilderInterface
from hatchling.plugin.manager import PluginManager

from pyside_app_build.config import PySideAppBuildConfig
from pyside_app_build.constants import TEMPLATE_ENV
from pyside_app_build.resource_generator import compile_qrc_to_resources


class PySideAppBuilder(BuilderInterface[PySideAppBuildConfig, PluginManager]):
    PLUGIN_NAME = "pyside-app"

    @classmethod
    def get_config_class(cls) -> type[BuilderConfig]:
        return PySideAppBuildConfig

    # --------------------------------------------------------------------------

    def clean(self, directory: str, versions: list[str]) -> None:
        pass

    # --------------------------------------------------------------------------

    def get_version_api(self) -> dict[str, Callable[..., str]]:
        return {
            "standard": self._build_standard,
        }

    # --------------------------------------------------------------------------

    def _build_standard(self, _: str, **__: Any) -> str:
        self.app.display_info("Building PySide App...")

        self.app.display_info("Compiling Qt Resources...")

        self.app.display_info("Packaging App Executable...")

        return ""

    # --------------------------------------------------------------------------

    def _compile_rcc(
        self,
        resource_target_dir: Path,
        extra_resource_root: list[Path] | None = None,
    ) -> Path:
        return compile_qrc_to_resources(
            target_dir=resource_target_dir,
            additional_resource_roots=[Path(r) for r in extra_resource_root or []],
            debug=self.app.verbosity >= 3,
        )

    def _render_deploy_template(self, repo_root: Path) -> None:
        pysidedeploy_template = TEMPLATE_ENV.get_template("pysidedeploy.spec.jinja2")

        spec_txt = pysidedeploy_template.render(
            {
                "icon": "xxx.png",
                "python_path": sys.executable,
            }
        )
        (repo_root / "pysidedeploy.spec").write_text(spec_txt)

    def _pyside_deploy(self, repo_root: Path) -> None:
        subprocess.check_call(
            [
                "pyside6-deploy",
                "--force",
                "--keep-deployment-files",
                "--c",
                str(repo_root / "pysidedeploy.spec"),
            ],
            text=True,
        )

    def _bundle_macos_dmg(
        self,
        exe_name: str,
        *,
        build_dir: Path,
        keep_build_files: bool = False,
    ) -> None:
        dmg_name = exe_name.replace(".app", ".dmg")

        dmg_target = build_dir / dmg_name
        dmg_target.unlink(missing_ok=True)

        subprocess.check_call(
            [
                "cd",
                str(build_dir),
                "&&",
                "hdiutil",
                "create",
                "-volname",
                exe_name,
                "-srcfolder",
                exe_name,
                "-ov",
                "-format",
                "UDZO",
                dmg_name,
            ],
            text=True,
        )

        if not keep_build_files:
            shutil.rmtree(build_dir / exe_name)

    def _linux_remove_bin_extension(
        self,
        exe_name: str,
        build_dir: Path,
    ) -> None:
        with_bin = build_dir / exe_name
        without_bin = build_dir / exe_name.removesuffix(".bin")

        with_bin.rename(without_bin)

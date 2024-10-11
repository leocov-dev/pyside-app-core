import platform
import re
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from hatchling.builders.config import BuilderConfig
from hatchling.builders.plugin.interface import BuilderInterface
from hatchling.plugin.manager import PluginManager
from pyside_app_build._custom_icon_gen import generate_project_icon
from pyside_app_build._pysidedeploy_spec_gen import build_deploy_spec
from pyside_app_build.config import PySideAppBuildConfig


class PySideAppBuilder(BuilderInterface[PySideAppBuildConfig, PluginManager]):
    PLUGIN_NAME = "pyside-app"

    @classmethod
    def get_config_class(cls) -> type[BuilderConfig]:
        return PySideAppBuildConfig

    # --------------------------------------------------------------------------

    def clean(self, directory: str, versions: list[str]) -> None:
        self._clean()

    def _clean(self):
        shutil.rmtree(self.config.dist_dir, ignore_errors=True)
        shutil.rmtree(self.config.build_dir, ignore_errors=True)
        self.config.dist_dir.mkdir(exist_ok=True)
        self.config.build_dir.mkdir(exist_ok=True)

    # --------------------------------------------------------------------------

    def get_version_api(self) -> dict[str, Callable[..., str]]:
        return {
            "standard": self._build_standard,
        }

    # --------------------------------------------------------------------------

    def _build_standard(self, _: str, **__: Any) -> str:
        self._clean()

        self.app.display_debug("Building PySide App...")

        if not self.config.icon.exists():
            self._gen_icon()

        spec_file = self._gen_spec_file()
        bundle_tmp = self._pyside_deploy(spec_file)

        app_build_bundle = self.config.build_dir / bundle_tmp.name

        shutil.move(bundle_tmp, app_build_bundle)
        shutil.move(self.config.spec_root / "deployment", self.config.build_dir / "deployment")

        self.app.display_debug("Packaging App Executable...")
        match plat := platform.system():
            case "Darwin":
                artifact = self._bundle_macos_dmg(app_build_bundle)
            case "Linux":
                artifact = self._linux_remove_bin_extension(app_build_bundle)
            case "Windows":
                artifact = self._win_copy(app_build_bundle)
            case _:
                raise Exception(f"Unsupported platform: {plat}")

        return str(artifact)

    # --------------------------------------------------------------------------

    def _gen_spec_file(self) -> Path:
        return build_deploy_spec(
            self.config.spec_root,
            entrypoint=self.config.entrypoint,
            icon=self.config.icon,
            extra_python_packages=self.config.extra_python_packages,
            extra_qt_modules=self.config.extra_qt_modules,
            extra_qt_plugins=self.config.extra_qt_plugins,
            macos_permissions=self.config.macos_permissions,
            extra_package_data=self.config.extra_package_data,
            extra_data_dirs=self.config.extra_data_dirs,
        )

    def _gen_icon(self) -> None:
        generate_project_icon(self.config.icon, self.config.entrypoint)


    def _pyside_deploy(self, spec_file: Path) -> Path:
        out = subprocess.run(
            [
                "pyside6-deploy",
                "--force",
                "--keep-deployment-files",
                "--c",
                str(spec_file),
            ],
            text=True,
            cwd=str(spec_file.parent),
            capture_output=True,
        )

        if self.app.verbosity >= 1:
            print(out.stdout)

        if out.returncode != 0:
            raise Exception(f"PySide Deploy failed: {out.stderr}")

        app_bundle = re.findall(
            r"\[DEPLOY] Executed file created in (.+)",
            out.stdout,
            re.MULTILINE
        )[0]
        self.app.display_debug(f"---> \"{app_bundle}\"")

        return Path(app_bundle)

    def _bundle_macos_dmg(
        self,
        app: Path,
    ) -> Path:
        app_name = app.name
        dmg_name = app_name.replace(".app", ".dmg")

        dmg_source = app.parent / dmg_name
        dmg_target = self.config.dist_dir / dmg_name
        dmg_target.unlink(missing_ok=True)

        out = subprocess.run(
            [
                "hdiutil",
                "create",
                "-volname",
                app_name,
                "-srcfolder",
                app_name,
                "-ov",
                "-format",
                "UDZO",
                dmg_name,
            ],
            text=True,
            cwd=str(app.parent),
            capture_output=True,
        )

        if self.app.verbosity >= 1:
            print(out.stdout)

        if out.returncode != 0:
            raise Exception(f"DMG Packaging failed: {out.stderr}")

        shutil.move(dmg_source, dmg_target)

        return dmg_target

    def _linux_remove_bin_extension(
        self,
        with_bin: Path,
    ) -> Path:
        without_bin = self.config.dist_dir / with_bin.name.removesuffix(".bin")

        shutil.copy(with_bin, without_bin)

        return without_bin

    def _win_copy(self, bundle: Path) -> Path:
        output = self.config.dist_dir / bundle.name

        shutil.copy(bundle, output)

        return output

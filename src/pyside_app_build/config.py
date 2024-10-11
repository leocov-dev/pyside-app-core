from pathlib import Path
from uuid import uuid4

from hatchling.builders.config import BuilderConfig


class PySideAppBuildConfig(BuilderConfig):
    """"""

    @property
    def dist_dir(self) -> Path:
        return Path(self.root) / "dist"

    @property
    def build_dir(self) -> Path:
        return Path(self.root) / "build"

    @property
    def icon(self) -> Path:
        return Path(self.root) / self.target_config.get("icon")

    @property
    def extra_python_packages(self) -> list[str]:
        return self.target_config.get("extra-python-packages", [])

    @property
    def extra_package_data(self) -> list[str]:
        return self.target_config.get("extra-package-data", [])

    @property
    def extra_qt_modules(self) -> list[str]:
        return self.target_config.get("extra-qt-modules", [])

    @property
    def extra_qt_plugins(self) -> list[str]:
        return self.target_config.get("extra-qt-plugins", [])

    @property
    def macos_permissions(self) -> list[str]:
        return self.target_config.get("macos-permissions", [])

    @property
    def extra_data_dirs(self) -> list[str]:
        return self.target_config.get("extra-data-dirs", [])

    @property
    def spec_root(self) -> Path:
        return Path(self.root) / self.target_config.get("spec-root")

    @property
    def entrypoint(self) -> str:
        entrypoint_file = Path(self.root) / self.target_config.get("entrypoint")
        return str(entrypoint_file.relative_to(self.spec_root))

    # @property
    # def target_config(self) -> dict[str, Any]:
    #     target_config = super().target_config
    #
    #     return {
    #         **target_config,
    #         "stuff": [],
    #     }

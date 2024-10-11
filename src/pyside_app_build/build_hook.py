from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

from pyside_app_build.resource_generator import compile_qrc_to_resources


class QtResourceBuildHook(BuildHookInterface):
    """ build Qt resources """

    PLUGIN_NAME = "pyside-app"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        project_root = Path(self.root)
        resource_target: str = self.config.get("resource-target", "")
        abs_target = project_root / resource_target

        if not abs_target.exists():
            raise Exception("resource-target dir does not exist")

        resource_roots: list[str] = self.config.get("extra-resource-roots", [])

        abs_roots = [
            project_root / r
            for r in resource_roots
        ]

        if any(not r.exists() for r in abs_roots):
            raise Exception("extra-resource-roots contained invalid paths")

        self.app.display_debug("Generating Qt resources...")
        self._compile_rcc(
            resource_target_dir=abs_target,
            extra_resource_root=abs_roots,
        )

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

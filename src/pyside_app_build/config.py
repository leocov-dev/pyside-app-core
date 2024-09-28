from typing import Any

from hatchling.builders.config import BuilderConfig


class PySideAppBuildConfig(BuilderConfig):
    """"""

    @property
    def target_config(self) -> dict[str, Any]:
        target_config = super().target_config

        return {
            **target_config,
            "stuff": [],
        }

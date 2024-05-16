from pathlib import Path
from typing import List

from pyside_app_core.resource_generator.generate_resources import (
    _compose_template_environment,
)


def _compile_qss_template(theme: QssTheme, qss_extra: List[Path] | None = None) -> str:
    qss_extra = qss_extra or []
    env = _compose_template_environment(*qss_extra)
    qss_template = env.get_template("style.qss.jinja2")
    return qss_template.render(theme=theme, qss_extra=[q.name for q in qss_extra])

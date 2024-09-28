from pathlib import Path

from jinja2 import Environment, FileSystemLoader

_root = Path(__file__).parent

TEMPLATES_DIR = _root / "templates"
RESOURCES_DIR = _root / "resources"

TEMPLATE_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)

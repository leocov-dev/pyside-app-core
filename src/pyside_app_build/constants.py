from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from pyside_app_core import resources

_root = Path(__file__).parent

TEMPLATES_DIR = _root / "templates"
RESOURCES_DIR = Path(resources.__file__).parent

TEMPLATE_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)

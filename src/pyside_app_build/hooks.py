from hatchling.plugin import hookimpl

from pyside_app_build.builder import PySideAppBuilder


@hookimpl
def hatch_register_builder() -> type[PySideAppBuilder]:
    return PySideAppBuilder

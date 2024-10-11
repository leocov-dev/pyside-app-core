from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.builders.plugin.interface import BuilderInterface
from hatchling.plugin import hookimpl

from pyside_app_build.build_hook import QtResourceBuildHook
from pyside_app_build.builder import PySideAppBuilder


@hookimpl
def hatch_register_builder() -> type[BuilderInterface]:
    return PySideAppBuilder


@hookimpl
def hatch_register_build_hook() -> type[BuildHookInterface]:
    return QtResourceBuildHook

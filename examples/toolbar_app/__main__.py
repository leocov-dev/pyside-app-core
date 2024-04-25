import argparse
import os
import sys
from pathlib import Path
from typing import Type

_root = Path(__file__).parent


def generate_theme(theme: Type["QssTheme"]):
    from pyside_app_core import theme_generator

    theme_generator.compile_qrc_to_resources(qss_theme=theme, target_dir=_root)


def main(theme: Type["QssTheme"]):
    # NOTE: these imports are lumped in here for the ability to
    # set PLATFORM_OVERRIDE from code, normally you would not need
    # to do this
    from pyside_app_core.errors import excepthook
    from pyside_app_core.qt import application_service
    from toolbar_app import __version__
    from toolbar_app.app import SimpleApp

    excepthook.install_excepthook()
    application_service.set_app_version(__version__)
    application_service.set_app_id("com.example.simple-app")
    application_service.set_app_name("Simple App")
    application_service.set_app_theme(theme())

    sys.exit(SimpleApp().launch())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=["mac", "win", "nix"])
    parser.add_argument("--generate-rcc", action="store_true")

    args = parser.parse_args()

    match args.style:
        case "mac":
            os.environ["PLATFORM_OVERRIDE"] = "Darwin"
        case "win":
            os.environ["PLATFORM_OVERRIDE"] = "Windows"
        case "nix":
            os.environ["PLATFORM_OVERRIDE"] = "Linux"

    from pyside_app_core.style.theme import QssTheme

    class CustomTheme(QssTheme):
        ...

    if args.generate_rcc:
        generate_theme(CustomTheme)

    main(CustomTheme)

import argparse
import os
import sys
from pathlib import Path

_root = Path(__file__).parent


def main(generate_rcc: bool):
    # NOTE: these imports are lumped in here for the ability to
    # override PLATFORM_OVERRIDE from code, normally would not do this
    from pyside_app_core.errors import excepthook
    from pyside_app_core.qt.style import QssTheme
    from pyside_app_core.services import application_service
    from simple_app import __version__
    from simple_app.app import SimpleApp

    class CustomTheme(QssTheme):
        ...

    excepthook.install_excepthook()
    application_service.set_app_version(__version__)
    application_service.set_app_id("com.example.simple-app")
    application_service.set_app_name("Simple App")
    application_service.set_app_theme(CustomTheme)

    if generate_rcc:
        from pyside_app_core import generator_utils

        generator_utils.compile_qrc_to_resources(
            qss_theme=CustomTheme, target_dir=_root
        )

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

    main(args.generate_rcc)

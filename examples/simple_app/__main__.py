import argparse
import sys
from pathlib import Path

from pyside_app_core.errors import excepthook
from pyside_app_core.qt.style import QssTheme
from pyside_app_core.services import application_service
from simple_app import __version__
from simple_app.app import SimpleApp

_root = Path(__file__).parent


class CustomTheme(QssTheme):
    """example custom theme, override or add new properties here"""


THEME = CustomTheme()


def main():
    application_service.set_app_version(__version__)
    application_service.set_app_id("com.example.simple-app")
    application_service.set_app_name("Simple App")
    application_service.set_app_theme(THEME)

    excepthook.install_excepthook()

    sys.exit(SimpleApp().launch())


def generate_style_and_resources():
    from pyside_app_core import generator_utils

    generator_utils.compile_qrc_to_resources(qss_theme=THEME, target_dir=_root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-rcc", action="store_true")

    args = parser.parse_args()

    if args.generate_rcc:
        generate_style_and_resources()

    main()

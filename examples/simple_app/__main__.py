import argparse
import sys
from pathlib import Path

from pyside_app_core.generator_utils.style_types import QssTheme

_root = Path(__file__).parent


class CustomTheme(QssTheme):
    pass


def main():
    from pyside_app_core.errors import excepthook
    from pyside_app_core.services import application_service
    from simple_app import __version__
    from simple_app.app import SimpleApp

    application_service.set_app_version(__version__)
    application_service.set_app_id("com.example.simple-app")
    application_service.set_app_name("Simple App")
    application_service.set_app_theme(CustomTheme())

    excepthook.install_excepthook()

    sys.exit(SimpleApp(_root / "resources.rcc").launch())


def generate_style_and_resources():
    from pyside_app_core import generator_utils

    generator_utils.compile_qrc_to_resources(target_dir=_root, rcc_format="binary")


if __name__ == '__main__':
    sys.path.append(str(_root.parent.parent / 'src'))

    parser = argparse.ArgumentParser()
    parser.add_argument('--generate-rcc', action='store_true')

    args = parser.parse_args()

    if args.generate_rcc:
        generate_style_and_resources()

    main()

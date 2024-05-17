import argparse
import os
from pathlib import Path

from pyside_app_core import log

_root = Path(__file__).parent


def compile_rcc() -> None:
    from pyside_app_core import resource_generator

    log.info("Generating resources...")

    resource_generator.compile_qrc_to_resources(target_dir=_root, debug=True)


def main() -> None:
    # NOTE: these imports are lumped in here for the ability to
    # set PLATFORM_OVERRIDE from code, normally you would not need
    # to do this
    from pyside_app_core.errors import excepthook
    from pyside_app_core.qt.standard.error_dialog import ErrorDialog
    from toolbar_app import __version__
    from toolbar_app.app import SimpleApp

    excepthook.install_excepthook(ErrorDialog)
    from pyside_app_core.qt.application_service import AppMetadata

    AppMetadata.init(
        "com.example.simple-app",
        "Simple App",
        __version__,
        help_url="https://github.com/leocov-dev/pyside-app-core",
        bug_report_url="https://github.com/leocov-dev/pyside-app-core/issues",
    )

    SimpleApp().launch()


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

    if args.generate_rcc:
        compile_rcc()

    main()

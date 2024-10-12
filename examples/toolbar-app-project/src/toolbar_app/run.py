from loguru import logger

from pyside_app_core.app.application_service import AppMetadata
from pyside_app_core.errors import excepthook
from pyside_app_core.log import configure_get_logger_func
from pyside_app_core.ui.standard.error_dialog import ErrorDialog
from toolbar_app import __version__
from toolbar_app.app import SimpleApp

configure_get_logger_func(lambda: logger)

excepthook.install_excepthook(ErrorDialog)
AppMetadata.init(
    "com.example.simple-app",
    "Simple App",
    __version__,
    icon_resource=":/tb/app/icon.png",
    help_url="https://github.com/leocov-dev/pyside-app-core",
    bug_report_url="https://github.com/leocov-dev/pyside-app-core/issues",
)

app = SimpleApp()


def run() -> None:
    app.launch()

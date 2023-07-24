def run_app():
    from pyside_app_core.services import application_service
    from simple_app.__main__ import THEME
    from simple_app import __version__

    application_service.set_app_version(__version__)
    application_service.set_app_id("com.example.simple-app")
    application_service.set_app_name("Simple App")
    application_service.set_app_theme(THEME)

    sys.exit(SimpleApp().launch())

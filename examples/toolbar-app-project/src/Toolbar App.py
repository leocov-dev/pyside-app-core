import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", choices=["mac", "win", "nix"])

    args = parser.parse_args()

    match args.style:
        case "mac":
            os.environ["PLATFORM_OVERRIDE"] = "Darwin"
        case "win":
            os.environ["PLATFORM_OVERRIDE"] = "Windows"
        case "nix":
            os.environ["PLATFORM_OVERRIDE"] = "Linux"

    # this is nested in here to allow the platform overrides above
    from toolbar_app.app import SimpleApp

    SimpleApp().launch()

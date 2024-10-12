import argparse
import os


def main():
    from toolbar_app import run

    run.run()


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

    main()

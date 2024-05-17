import argparse
from pathlib import Path

from pyside_app_core.resource_generator import compile_qrc_to_resources


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--extra-resource-root",
        help="Provide a root path to search for additional QResource files " "(Can specify this flag multiple times)",
        action="append",
    )

    parser.add_argument(
        "target_dir",
        help="Provide a directory path were the final resource file will be placed",
        metavar="target-dir",
    )

    parser.add_argument(
        "--debug",
        help="print the contents of the qrc file to stdout",
        action="store_true",
    )

    args = parser.parse_args()

    print("...")

    generated_file = compile_qrc_to_resources(
        target_dir=Path(args.target_dir),
        additional_resource_roots=[Path(r) for r in args.extra_resource_root or []],
        debug=args.debug,
    )

    print(f'Generated: "{generated_file}"')


if __name__ == "__main__":
    main()

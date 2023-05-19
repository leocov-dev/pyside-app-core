import argparse
import importlib
import os.path
import sys
from pathlib import Path

from pyside_app_core.generator_utils import compile_qrc_to_resources
from pyside_app_core.qt.style import DEFAULT_THEME


def main():
    parser = argparse.ArgumentParser("compile-pyside-theme")

    parser.add_argument(
        "--extra-python-path",
        help="Provide a directory path to resolve python imports",
    )
    parser.add_argument(
        "--custom-theme",
        help='Provide a python module path for a custom theme object e.g. "my.theme.CustomTheme"',
    )
    parser.add_argument(
        "--extra-qss-templates",
        help='Provide file path to jinja template for qss e.g. "my/theme/templates/custom.qss.jinja2" (Can specify this flag multiple times)',
        action="append",
    )
    parser.add_argument(
        "--extra-qresources",
        help='Provide a python module path for additional QResource object e.g. "my.theme.Resource" (Can specify this flag multiple times)',
        action="append",
    )

    parser.add_argument(
        "target_dir",
        help="Provide a directory path were the final resource file will be placed",
        metavar="target-dir",
    )

    args = parser.parse_args()

    print("...")

    target_dir = Path(args.target_dir)

    if args.extra_python_path:
        pypath = os.path.abspath(args.extra_python_path)
        sys.path.append(pypath)

    theme = DEFAULT_THEME
    if args.custom_theme:
        mod_path, klass_name = args.custom_theme.rsplit(".", 1)

        mod = importlib.import_module(mod_path)

        theme = getattr(mod, klass_name)

    qss_template_extra = None
    if args.extra_qss_templates:
        qss_template_extra = [Path(q) for q in args.extra_qss_templates]

    resources_extra = []
    if args.extra_qresources:
        for rcc in args.extra_qresources:
            mod_path, obj_name = rcc.rsplit(".", 1)

            mod = importlib.import_module(mod_path)

            resources_extra.append(getattr(mod, obj_name))

    generated_file = compile_qrc_to_resources(
        target_dir=target_dir,
        qss_theme=theme,
        qss_template_extra=qss_template_extra,
        resources_extra=resources_extra,
    )

    print(f'Generated: "{generated_file}"')


if __name__ == "__main__":
    main()

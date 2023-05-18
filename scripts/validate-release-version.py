import os
import sys
import tomllib
from pathlib import Path

__repo = Path(__file__).parent.parent

if __name__ == "__main__":
    sys.path.append(str(__repo / "src"))
    from pyside_app_core import __version__ as src_version

    tag_version = os.environ.get("TAG", "")

    with open(__repo / "pyproject.toml", "rb") as ppt:
        project_version = tomllib.load(ppt)["project"]["version"]

    if not (project_version == tag_version == src_version):
        print("versions did not match:")
        print(f"project: {project_version}")
        print(f"tag:     {tag_version}")
        print(f"src:     {src_version}")
        sys.exit(1)

    print(f"version strings <{project_version}> OK")

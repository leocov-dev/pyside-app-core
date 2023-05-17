__version__ = "1.0.0"

# these path modifications are only here to make local development easy
# when using `pyside-app-core` as a library this is not needed
import sys
from pathlib import Path

__lib = Path(__file__).parent.parent.parent / "src"
__root = Path(__file__).parent.parent

sys.path.extend([str(__lib), str(__root)])

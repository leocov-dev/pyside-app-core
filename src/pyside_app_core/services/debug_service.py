import inspect
from pathlib import Path


def get_caller_file(depth: int = 3) -> Path:
    # TODO: not sure this will reliably find the entrypoint
    # cur_frame = inspect.currentframe()
    # call_frame = inspect.getouterframes(cur_frame, frame)
    return Path(inspect.stack()[depth].filename)

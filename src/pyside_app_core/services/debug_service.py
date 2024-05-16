import inspect
from pathlib import Path


def get_caller_file(frame: int = 2, depth: int = 3) -> Path:
    # TODO: not sure this will reliably find the entrypoint
    cur_frame = inspect.currentframe()
    call_frame = inspect.getouterframes(cur_frame, frame)
    return Path(call_frame[depth].filename)

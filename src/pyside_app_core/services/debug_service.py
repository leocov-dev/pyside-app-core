import inspect
from pathlib import Path


def get_caller_file():
    # TODO: not sure this will reliably find the entrypoint
    cur_frame = inspect.currentframe()
    call_frame = inspect.getouterframes(cur_frame, 2)
    return Path(call_frame[3].filename)

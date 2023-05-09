from app_style.constants import LIST_DATA_LEN_MAX
from app_style.errors.basic_errors import CoreError


class EncodingListError(CoreError):
    def __init__(self, actual_len: int):
        super(EncodingListError, self).__init__(
            f"command data list was too long, max: {LIST_DATA_LEN_MAX}, actual: {actual_len}",
            internal=True,
        )

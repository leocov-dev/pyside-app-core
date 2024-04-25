from typing import Literal

from pyside_app_core.types.numeric import FloatPrecision

# ------------------------------------------------------------------------------
# defined values
DATA_ENCODING_ENDIAN: Literal["little"] = "little"
LIST_DATA_LEN_BYTES = 2
FLOAT_PRECISION: FloatPrecision = "single"

# ------------------------------------------------------------------------------
# calculated values
DATA_STRUCT_ENDIAN = "<" if DATA_ENCODING_ENDIAN == "little" else ">"
STRUCT_FLOAT_FMT = "f" if FLOAT_PRECISION == "single" else "d"

LIST_DATA_LEN_BITS = 8 * LIST_DATA_LEN_BYTES
LIST_DATA_LEN_MAX = pow(2, LIST_DATA_LEN_BITS) - 1

# ------------------------------------------------------------------------------
COBS_SEP = b"\x00"
BUTTON_HEIGHT = 30

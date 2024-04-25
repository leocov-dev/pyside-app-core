import struct
from typing import List

from pyside_app_core.constants import (
    DATA_ENCODING_ENDIAN,
    LIST_DATA_LEN_MAX,
    DATA_STRUCT_ENDIAN,
    LIST_DATA_LEN_BYTES,
    FLOAT_PRECISION,
)
from pyside_app_core.errors.encode_errors import EncodingListError
from pyside_app_core.types.numeric import FloatPrecision


def int_to_bytes(val: int, num_bytes: int, signed: bool) -> bytes:
    return val.to_bytes(length=num_bytes, byteorder=DATA_ENCODING_ENDIAN, signed=signed)


def int_from_bytes(val: bytes, signed: bool) -> int:
    return int.from_bytes(bytes=val, byteorder=DATA_ENCODING_ENDIAN, signed=signed)


def encode_float_list(
    floats: List[float], precision: FloatPrecision = FLOAT_PRECISION
) -> bytearray:
    data_len = len(floats)
    if data_len > LIST_DATA_LEN_MAX:
        raise EncodingListError(data_len)

    precision_format = "f" if precision == "single" else "d"

    encoded = bytearray()
    encoded.extend(int_to_bytes(data_len, LIST_DATA_LEN_BYTES, False))
    encoded.extend(
        struct.pack(f"{DATA_STRUCT_ENDIAN}{data_len}{precision_format}", *floats)
    )

    return encoded


def decode_float_list(
    raw_data: bytes, precision: FloatPrecision = FLOAT_PRECISION
) -> List[float]:
    len_bytes = raw_data[:LIST_DATA_LEN_BYTES]
    data_bytes = raw_data[LIST_DATA_LEN_BYTES:]

    precision_format = "f" if precision == "single" else "d"

    data_len = int_from_bytes(len_bytes, False)
    return list(
        struct.unpack(f"{DATA_STRUCT_ENDIAN}{data_len}{precision_format}", data_bytes)
    )

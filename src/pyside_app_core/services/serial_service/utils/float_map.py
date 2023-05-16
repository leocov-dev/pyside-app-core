import struct
from decimal import Decimal
from typing import Any, Iterator, Mapping, Self, TypeVar

from pyside_app_core.constants import DATA_STRUCT_ENDIAN, FLOAT_PRECISION, STRUCT_FLOAT_FMT

K = TypeVar("K", bound=int)


class FloatMap(Mapping[K, float]):
    def __init__(self, data: Mapping[K, float]):
        self._data = data

    def __getitem__(self, k: K) -> float:
        return self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    @classmethod
    def _key_xform(cls, key: int) -> Any:
        return key

    def pack(self) -> bytearray:
        """
        pattern:
        count,key,value,key,value,key,value,...
        b - count, number of pairs - max 255 params...
        b - key in 1 byte corresponding to enum ConfigurationParam
        f/d - value in 4 or 8 bytes corresponding to float/double value
        example
        struct.pack("<bbfbf", count, key, value, key, value)
        """
        if not self._data:
            raise AttributeError("Command had no data")

        accum_fmt = ""
        flattened_data = []

        for key, value in self._data.items():
            accum_fmt += f"b{STRUCT_FLOAT_FMT}"
            flattened_data.extend([key, value])

        raw = struct.pack(
            f"{DATA_STRUCT_ENDIAN}b{accum_fmt}", len(self._data), *flattened_data
        )
        return bytearray(raw)

    @classmethod
    def unpack(cls, raw_data: bytes) -> Self:
        raw_pair_count = raw_data[:1]
        raw_key_val = raw_data[1:]

        pair_count = utils.int_from_bytes(raw_pair_count, signed=False)
        fmt_chars = ["b", STRUCT_FLOAT_FMT] * pair_count

        flat_pairs = struct.unpack(
            f"{DATA_STRUCT_ENDIAN}{''.join(fmt_chars)}", raw_key_val
        )

        data = {}
        iterable = iter(flat_pairs)

        for key in iterable:
            val = next(iterable)
            if FLOAT_PRECISION == "single":
                val = float(Decimal(val).quantize(Decimal("0.000000")))
            data[cls._key_xform(key)] = val

        return cls(data=data)

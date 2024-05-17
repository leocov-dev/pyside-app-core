import struct
from collections.abc import Iterator, Mapping
from decimal import Decimal
from typing import Any, TypeVar

from pyside_app_core.constants import (
    DATA_STRUCT_ENDIAN,
    FLOAT_PRECISION,
    STRUCT_FLOAT_FMT,
)
from pyside_app_core.services.serial_service import conversion_utils
from pyside_app_core.utils import compare

K = TypeVar("K", bound=int)

_TWO_BYTE_LEN = 65535


class FloatMap(Mapping[K, float]):
    _count_fmt = "H"  # unsigned short, 2 bytes
    _key_fmt = "H"  # unsigned short, 2 bytes

    def __init__(self, data: Mapping[K, float]):
        self._data = data

        if not data:
            raise ValueError(f"can't create an empty {self.__class__.__name__}")

        if len(data) > _TWO_BYTE_LEN:
            raise ValueError("data has too many values, must fit in 2 bytes")

        for k in data:
            if k > _TWO_BYTE_LEN:
                raise ValueError(f'key: "{k}" does not fit in 2 bytes')

            if k < 0:
                raise ValueError(f'key: "{k}" is not a positive number')

    def __getitem__(self, k: K) -> float:
        return self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __repr__(self) -> str:
        return self._data.__repr__()

    def __str__(self) -> str:
        return self._data.__str__()

    def __eq__(self, other: "FloatMap[K]") -> bool:  # type: ignore[override]
        val_eq: list[bool] = []
        for k, v in self.items():
            other_v = other.get(k)
            if other_v:
                val_eq.append(compare.float_approx(v, other_v))

        return all(
            [
                sorted(self.keys()) == sorted(other.keys()),
                *val_eq,
            ]
        )

    @classmethod
    def _key_xform(cls, key: int) -> Any:
        return key

    @classmethod
    def pack_format(cls, item_count: int) -> str:
        if item_count < 1:
            raise ValueError("must pack at least 1 item")

        accum_fmt = f"{DATA_STRUCT_ENDIAN}{cls._count_fmt}"

        accum_fmt += f"{cls._key_fmt}{STRUCT_FLOAT_FMT}" * item_count

        return accum_fmt

    def pack(self) -> bytearray:
        """
        pattern:
        count,key,value,key,value,key,value,...
        H - count, number of pairs - max 2 bytes unsigned...
        H - key in 2 bytes corresponding to enum ConfigurationParam
        f/d - value in 4 or 8 bytes corresponding to float/double value

        example:
        struct.pack("<HHfHf", count, key, value, key, value)
        """
        if not self._data:
            raise AttributeError("Command had no data")

        count = len(self)
        flattened_data = []

        for key, value in self._data.items():
            flattened_data.extend([key, value])

        raw = struct.pack(self.pack_format(count), count, *flattened_data)
        return bytearray(raw)

    @classmethod
    def unpack(cls, raw_data: bytes) -> "FloatMap[K]":
        count_bytes = 2
        raw_pair_count = raw_data[:count_bytes]
        raw_key_val = raw_data[count_bytes:]

        pair_count = conversion_utils.int_from_bytes(raw_pair_count, signed=False)
        fmt_chars = [cls._key_fmt, STRUCT_FLOAT_FMT] * pair_count

        flat_pairs = struct.unpack(f"{DATA_STRUCT_ENDIAN}{''.join(fmt_chars)}", raw_key_val)

        data = {}
        iterable = iter(flat_pairs)

        for key in iterable:
            val = next(iterable)
            if FLOAT_PRECISION == "single":
                val = float(Decimal(val).quantize(Decimal("0.000000")))
            data[cls._key_xform(key)] = val

        return cls(data=data)

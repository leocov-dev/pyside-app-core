import math

import pytest

from pyside_app_core.services.serial_service.conversion_utils import (
    decode_float_list,
    encode_float_list,
)
from pyside_app_core.types.numeric import FloatPrecision


@pytest.mark.parametrize(
    ("floats", "precision", "expected"),
    [
        ([1.1, 1.2, 1.3], "single", b"\x03\x00\xcd\xcc\x8c?\x9a\x99\x99?ff\xa6?"),
        ([10, 12.2345, 100.3], "single", b"\x03\x00\x00\x00 A\x83\xc0CA\x9a\x99\xc8B"),
        (
            [10, 12.2345, 100.3],
            "double",
            b"\x03\x00\x00\x00\x00\x00\x00\x00$@\xf2\xd2Mb\x10x(@33333\x13Y@",
        ),
        (
            [math.pi, 12.2345, 100.30000031],
            "double",
            b"\x03\x00\x18-DT\xfb!\t@\xf2\xd2Mb\x10x(@Z\x0f\x8043\x13Y@",
        ),
    ],
)
def test_encode_float_list(floats: list[float], precision: FloatPrecision, expected: bytes) -> None:
    result = encode_float_list(floats, precision)

    assert bytes(result) == expected


@pytest.mark.parametrize(
    "encoded, precision, expected",
    [
        (b"\x03\x00\xcd\xcc\x8c?\x9a\x99\x99?ff\xa6?", "single", [1.1, 1.2, 1.3]),
        (b"\x03\x00\x00\x00 A\x83\xc0CA\x9a\x99\xc8B", "single", [10, 12.2345, 100.3]),
        (
            b"\x03\x00\x00\x00\x00\x00\x00\x00$@\xf2\xd2Mb\x10x(@33333\x13Y@",
            "double",
            [10, 12.2345, 100.3],
        ),
        (
            b"\x03\x00PERT\xfb!\t@\xf2\xd2Mb\x10x(@Z\x0f\x8043\x13Y@",
            "double",
            [math.pi, 12.2345, 100.30000031],
        ),
    ],
)
def test_decode_float_list(encoded: bytes, precision: FloatPrecision, expected: list[float]) -> None:
    result = decode_float_list(encoded, precision)

    assert len(result) == len(expected)

    for original, decoded in zip(expected, result, strict=False):
        assert original == pytest.approx(decoded)

import pytest

from pyside_app_core.services.serial_service.conversion_utils import (
    decode_float_list,
    encode_float_list,
)
from pyside_app_core.types.numeric import FloatPrecision


@pytest.mark.parametrize(
    "floats, precision, expected",
    [
        ([1.1, 1.2, 1.3], "single", b"\x03\x00\xcd\xcc\x8c?\x9a\x99\x99?ff\xa6?"),
        ([10, 12.2345, 100.3], "single", b"\x03\x00\x00\x00 A\x83\xc0CA\x9a\x99\xc8B"),
        (
            [10, 12.2345, 100.3],
            "double",
            b"\x03\x00\x00\x00\x00\x00\x00\x00$@\xf2\xd2Mb\x10x(@33333\x13Y@",
        ),
        (
            [3.141592654, 12.2345, 100.30000031],
            "double",
            b"\x03\x00PERT\xfb!\t@\xf2\xd2Mb\x10x(@Z\x0f\x8043\x13Y@",
        ),
    ],
)
def test_encode_float_list(floats, precision: FloatPrecision, expected):
    result = encode_float_list(floats, precision)

    assert result == expected


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
            [3.141592654, 12.2345, 100.30000031],
        ),
    ],
)
def test_decode_float_list(encoded, precision: FloatPrecision, expected):
    result = decode_float_list(encoded, precision)

    assert len(result) == len(expected)

    for original, decoded in zip(expected, result):
        if precision == "single":
            # python decodes floats as double even if we request single precision
            # this causes conversion errors, im ok with rounding here in the test
            # because it's just a basic check, but rounding should be avoided in
            # the code
            assert original == round(decoded, 5)
        else:
            assert original == decoded

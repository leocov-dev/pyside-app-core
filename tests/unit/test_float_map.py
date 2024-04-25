import pytest

from pyside_app_core.services.serial_service.float_map import FloatMap


def test_float_map__init():
    fm = FloatMap(
        {
            1: 1.0,
            2: 2.0,
            3: 3.0,
        }
    )

    assert fm[1] == 1.0
    assert fm[2] == 2.0
    assert fm[3] == 3.0
    assert len(fm) == 3

    with pytest.raises(KeyError):
        _ = fm[99]

    with pytest.raises(ValueError) as ee:
        FloatMap({})
    assert str(ee.value) == "can't create an empty FloatMap"

    with pytest.raises(ValueError) as ve:
        FloatMap({key: 1.0 for key in range(65536)})
    assert str(ve.value) == "data has too many values, must fit in 2 bytes"

    with pytest.raises(ValueError) as ke:
        FloatMap({key: 1.0 for key in range(60000, 70000)})
    assert str(ke.value) == 'key: "65536" does not fit in 2 bytes'

    with pytest.raises(ValueError) as se:
        FloatMap({-1: 1.0})
    assert str(se.value) == 'key: "-1" is not a positive number'

    for k, v in fm.items():
        assert k == v  # incidental, just want to be able to assert in loop


@pytest.mark.parametrize(
    "count, expected",
    [
        (1, f"<HHf"),
        (2, f"<HHfHf"),
        (3, f"<HHfHfHf"),
        (0, None),
    ],
)
def test_float_map__pack_format(count, expected):
    if count < 1:
        with pytest.raises(ValueError):
            FloatMap.pack_format(count)
    else:
        result = FloatMap.pack_format(count)
        assert result == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ({1: 1.0}, b"\x01\x00\x01\x00\x00\x00\x80?"),
        ({1: 1.0, 2: 2.0}, b"\x02\x00\x01\x00\x00\x00\x80?\x02\x00\x00\x00\x00@"),
        (
            {1: 1.0, 2: 2.0, 3: 3.0},
            b"\x03\x00\x01\x00\x00\x00\x80?\x02\x00\x00\x00\x00@\x03\x00\x00\x00@@",
        ),
    ],
)
def test_float_map__pack(data, expected):
    result = FloatMap(data).pack()
    assert result == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        (b"\x01\x00\x01\x00\x00\x00\x80?", {1: 1.0}),
        (b"\x02\x00\x01\x00\x00\x00\x80?\x02\x00\x00\x00\x00@", {1: 1.0, 2: 2.0}),
        (
            b"\x03\x00\x01\x00\x00\x00\x80?\x02\x00\x00\x00\x00@\x03\x00\x00\x00@@",
            {1: 1.0, 2: 2.0, 3: 3.0},
        ),
    ],
)
def test_float_map__unpack(raw, expected):
    result = FloatMap.unpack(raw)
    assert result == expected

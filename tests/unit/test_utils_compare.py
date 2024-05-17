import pytest

from pyside_app_core.utils import compare


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 1, True),
        (1.0, 1.0, True),
        (1.000001, 1.000001, True),
        (1.0, 1.000001, True),
        (1.0, 1.00001, False),
        (1.0, 1.1, False),
        (100000000.0, 100000000.0, True),
        (100000000.0, 100000000.0000001, True),
        (100000000.0, 100000000.00001, False),
    ],
)
def test_utils_compare_float_approx(a: float, b: float, expected: bool) -> None:
    result = compare.float_approx(a, b)
    assert result == expected

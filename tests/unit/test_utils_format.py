import pytest

from pyside_app_core.utils import strings


@pytest.mark.parametrize(
    ("width", "padded", "text", "expected"),
    [
        (80, False, "", ""),
        (10, False, "12345", "12345"),
        (10, True, "12345", "12345     "),
        (5, False, "12345678910", "12345\n67891\n0"),
        (5, False, "12345\n678910", "12345\n67891\n0"),
        (5, False, "12345678\n910", "12345\n678\n910"),
        (5, True, "12345678\n910", "12345\n678  \n910  "),
    ],
)
def test_wrap_text(width: int, padded: bool, text: str, expected: str) -> None:
    result = strings.wrap_text(text, width=width, padded=padded)
    assert result == expected

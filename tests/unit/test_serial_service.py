from typing import Self

from pytest_mock import MockerFixture

from pyside_app_core.services.serial_service.service import SerialService


class MockCommand:
    def __init__(self, data: str):
        self._data = data

    def __repr__(self):
        return f"MockCommand<{self._data}>"

    def __eq__(self, other):
        return self._data == other._data

    def encode(self) -> bytearray:
        return bytearray(self._data.encode("utf-8"))

    @classmethod
    def decode(cls, raw_data: bytes) -> Self:
        return cls(raw_data.decode("utf-8"))


class MockDecoder:
    @classmethod
    def decode_data(cls, data: bytearray) -> MockCommand:
        return MockCommand.decode(data)

    @classmethod
    def format_error(cls, error: Exception) -> MockCommand:
        return MockCommand()


def test_serial_service_buffering(mocker: MockerFixture):
    """
    check that cors segmentation and buffering is proper.
    if we get partial messages we will buffer until the null bit terminator
    is read and emit only complete chunks.
    """
    svc = SerialService(transcoder=MockDecoder(), parent=None)

    mock_com = mocker.patch.object(svc, "_com")
    mock_data_sig = mocker.patch.object(svc, "data")

    # list of individual data reads from com port
    mock_com.readAll.side_effect = [
        b"abc\x00",
        b"123",
        b"xyz\x00987",
        b"654\x00abc\x00AAA",
    ]

    svc._on_data()
    mock_data_sig.emit.assert_called_once_with(MockCommand("abc"))
    assert mock_data_sig.emit.call_count == 1

    svc._on_data()
    assert svc._buffer == b"123"
    assert mock_data_sig.emit.call_count == 1

    svc._on_data()
    mock_data_sig.emit.assert_called_with(MockCommand("123xyz"))
    assert svc._buffer == b"987"
    assert mock_data_sig.emit.call_count == 2

    svc._on_data()
    mock_data_sig.emit.assert_any_call(MockCommand("987654"))
    mock_data_sig.emit.assert_called_with(MockCommand("abc"))
    assert svc._buffer == b"AAA"
    assert mock_data_sig.emit.call_count == 4

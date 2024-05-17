from PySide6.QtCore import QObject
from pytest_mock import MockerFixture

from pyside_app_core.services.serial_service.service import SerialService
from pyside_app_core.services.serial_service.types import (
    ChunkedData,
    Decodable,
    Encodable,
)


class MockCommand(Encodable, Decodable):
    def __init__(self, data: str):
        self._data = data

    def __repr__(self) -> str:
        return f"MockCommand<{self._data}>"

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MockCommand):
            return self._data == other._data
        raise TypeError(f"Can't compare type: {type(other)} to {self.__class__.__name__}")

    def encode(self) -> bytes:
        return self._data.encode("utf-8")

    @classmethod
    def decode(cls, data: bytes) -> "MockCommand":
        return cls(data.decode("utf-8"))


class MockDecoder:
    @classmethod
    def process_buffer(cls, buffer: bytearray) -> ChunkedData:
        if b"\x00" in buffer:
            chunks: list[bytearray]
            remainder: bytearray
            *chunks, remainder = buffer.split(b"\x00")
            return chunks, remainder

        return [], None

    @classmethod
    def encode(cls, data: MockCommand) -> bytes:
        return data.encode()

    @classmethod
    def decode(cls, raw: bytearray) -> MockCommand:
        return MockCommand.decode(raw)


def test_serial_service_buffering(mocker: MockerFixture) -> None:
    """
    check that cors segmentation and buffering is proper.
    if we get partial messages we will buffer until the null bit terminator
    is read and emit only complete chunks.
    """
    svc = SerialService(transcoder=MockDecoder, parent=QObject())  # type: ignore[arg-type]

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

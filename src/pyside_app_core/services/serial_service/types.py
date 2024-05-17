from collections.abc import Sequence
from typing import Protocol

from PySide6.QtCore import Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


class Encodable(Protocol):
    def encode(self) -> bytes: ...

    def __str__(self) -> str: ...


class Decodable(Protocol):
    @classmethod
    def decode(cls, data: bytes) -> "Decodable": ...

    def __str__(self) -> str: ...


ChunkedData = tuple[Sequence[bytearray], bytearray | None]


class TranscoderInterface(Protocol):
    @classmethod
    def process_buffer(cls, buffer: bytearray) -> ChunkedData: ...

    @classmethod
    def encode(cls, data: Encodable) -> bytes: ...

    @classmethod
    def decode(cls, raw: bytearray) -> Decodable: ...


class SerialReader(Protocol):
    @Slot()
    def handle_serial_connect(self, com: QSerialPort) -> None: ...

    @Slot()
    def handle_serial_disconnect(self) -> None: ...

    @Slot()
    def handle_serial_ports(self, ports: list[QSerialPortInfo]) -> None: ...

    @Slot()
    def handle_serial_data(self, data: Decodable) -> None: ...

    @Slot()
    def handle_serial_error(self, error: Exception) -> None: ...


class PortFilter(Protocol):
    def __call__(self, ports: list[QSerialPortInfo]) -> list[QSerialPortInfo]: ...

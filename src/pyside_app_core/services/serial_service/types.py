import abc
from typing import Generic, Protocol, Self, Sequence, TypeVar
from pyside_app_core.services import serial_service

from PySide6.QtCore import Signal, Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


class Encodable(Protocol):
    def encode(self) -> bytearray:
        ...

    def __str__(self) -> str:
        ...


class Decodable(Protocol):
    @classmethod
    def decode(cls, data: bytes) -> Self:
        ...

    def __str__(self) -> str:
        ...


_TC = TypeVar("_TC", bound=Encodable, covariant=True)
_TR = TypeVar("_TR", bound=Decodable, covariant=True)

ChunkedData = tuple[Sequence[bytearray], bytearray | None]


class TranscoderInterface(Protocol[_TC, _TR]):
    @classmethod
    def process_buffer(cls, buffer: bytearray) -> ChunkedData:
        ...

    @classmethod
    def encode(cls, data: Encodable) -> bytearray:
        ...

    @classmethod
    def decode(cls, raw: bytearray) -> _TR:
        ...


class CanRegister(Protocol):
    def bind_serial_service(self, service: "serial_service.SerialService"):
        ...


class SerialReader(abc.ABC, Generic[_TR]):
    refresh_ports: Signal

    @Slot()
    def handle_serial_connect(self, com: QSerialPort) -> None:
        pass

    @Slot()
    def handle_serial_disconnect(self) -> None:
        pass

    @Slot()
    def handle_serial_ports(self, ports: list[QSerialPortInfo]) -> None:
        pass

    @Slot()
    def handle_serial_data(self, data: Decodable) -> None:
        pass

    @Slot()
    def handle_serial_error(self, error: Exception) -> None:
        pass


class PortFilter(Protocol):
    def __call__(self, ports: list[QSerialPortInfo]) -> list[QSerialPortInfo]:
        ...

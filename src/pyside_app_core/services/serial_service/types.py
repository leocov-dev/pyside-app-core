import abc
from typing import Protocol, Sequence

from PySide6.QtCore import Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from pyside_app_core.services import serial_service


class Encodable(abc.ABC):
    @abc.abstractmethod
    def encode(self) -> bytes:
        return NotImplementedError

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"


class Decodable(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def decode(cls, data: bytes) -> "Decodable":
        raise NotImplementedError

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"


ChunkedData = tuple[Sequence[bytearray], bytearray | None]


class TranscoderInterface(Protocol):
    @classmethod
    def process_buffer(cls, buffer: bytearray) -> ChunkedData:
        ...

    @classmethod
    def encode(cls, data: Encodable) -> bytes:
        ...

    @classmethod
    def decode(cls, raw: bytearray) -> Decodable:
        ...


class CanRegister(Protocol):
    def bind_serial_service(self, service: "serial_service.SerialService") -> None:
        ...


class SerialReader(Protocol):
    @Slot()
    def handle_serial_connect(self, com: QSerialPort) -> None:
        ...

    @Slot()
    def handle_serial_disconnect(self) -> None:
        ...

    @Slot()
    def handle_serial_ports(self, ports: list[QSerialPortInfo]) -> None:
        ...

    @Slot()
    def handle_serial_data(self, data: Decodable) -> None:
        ...

    @Slot()
    def handle_serial_error(self, error: Exception) -> None:
        ...


class PortFilter(Protocol):
    def __call__(self, ports: list[QSerialPortInfo]) -> list[QSerialPortInfo]:
        ...

import logging
from typing import List, Protocol

from PySide6.QtCore import QIODevice, QObject, Qt, QTimer, Signal
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from pyside_app_core import log
from pyside_app_core.errors.serial_errors import (
    SerialConnectionError,
    SerialDisconnectedError,
    SerialReadError,
    SerialUnknownError,
    SerialWriteError,
)
from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.services.serial_service.utils.abstract_decoder import DecoderInterface

log.set_level(lvl=logging.DEBUG)


class CanRegister(Protocol):
    def bind_serial_service(self, serial_service: "SerialService"):
        ...


class SerialService(ObjectNameMixin, QObject):
    ports = Signal(list)
    com_connect = Signal(QSerialPort)
    com_disconnect = Signal()
    data = Signal(object)
    error = Signal(Exception)

    def __init__(self, decoder: DecoderInterface, parent: QObject):
        super(SerialService, self).__init__(parent=parent)

        self._decoder = decoder
        self._com: QSerialPort | None = None
        self._buffer = bytearray()

    def _open(
        self, port_info: QSerialPortInfo
    ) -> tuple[QSerialPort, QSerialPort.SerialPortError | None]:
        com = QSerialPort(port_info, parent=self)
        com.setBaudRate(QSerialPort.BaudRate.Baud115200)
        open_ok = com.open(QIODevice.OpenModeFlag.ReadWrite)

        return com, None if open_ok else com.error()

    def _close(self, com: QSerialPort | None) -> None:
        if com and com.isOpen():
            com.flush()
            com.close()

    def open_connection(self, port_info: QSerialPortInfo) -> bool:
        self.close_connection()

        self._com, error = self._open(port_info)
        if error:
            self._on_error(error)
            return False

        self._com.readyRead.connect(self._on_data)
        self._com.errorOccurred.connect(self._on_error)

        self.com_connect.emit(self._com)

        return True

    def register_reader(self, reader: QObject) -> None:
        if hasattr(reader, "handle_serial_connect"):
            self.com_connect[QSerialPort].connect(
                reader.handle_serial_connect,
                type=Qt.ConnectionType.UniqueConnection,
            )
        if hasattr(reader, "handle_serial_disconnect"):
            self.com_disconnect.connect(
                reader.handle_serial_disconnect,
                type=Qt.ConnectionType.UniqueConnection,
            )
        if hasattr(reader, "handle_serial_ports"):
            self.ports[list].connect(
                reader.handle_serial_ports,
                type=Qt.ConnectionType.UniqueConnection,
            )
        if hasattr(reader, "handle_serial_data"):
            self.data[bytearray].connect(
                reader.handle_serial_data,
                type=Qt.ConnectionType.UniqueConnection,
            )
        if hasattr(reader, "handle_serial_error"):
            self.error[Exception].connect(
                reader.handle_serial_error,
                type=Qt.ConnectionType.UniqueConnection,
            )

    def link(self, *can_register: CanRegister):
        for item in can_register:
            item.bind_serial_service(self)

    def scan_for_ports(self) -> None:
        ports = QSerialPortInfo.availablePorts()

        self._debug_ports(ports)
        log.debug("sending ports...")

        self.ports.emit([p for p in ports if self._port_filter(p)])

    def close_connection(self) -> None:
        if self._com:
            self.com_disconnect.emit()

            try:
                self._com.errorOccurred.disconnect()
                self._com.readyRead.disconnect()
            except Exception as e:
                log.exception(e)
                pass

            self._close(self._com)
            self._com.deleteLater()
            self._com = None

    def deleteLater(self) -> None:
        self.close_connection()
        super().deleteLater()

    def _on_data(self, *args, **kwargs) -> None:
        read: bytes = self._com.readAll()
        data = bytearray(read)
        self._buffer.extend(data)

        if b"\x00" in self._buffer:
            chunks: list[bytearray]
            remainder: bytearray
            *chunks, remainder = self._buffer.split(b"\x00")

            for chunk in chunks:
                try:
                    command = self._decoder.decode_data(chunk)
                except Exception as e:
                    log.exception(e)
                    command = self._decoder.format_error(e)

                self.data.emit(command)

            self._buffer.clear()
            self._buffer.extend(remainder)

    def _on_error(self, error: QSerialPort.SerialPortError | None) -> None:
        if error is None or error == QSerialPort.SerialPortError.NoError:
            return
        elif error == QSerialPort.SerialPortError.OpenError:
            exception = SerialConnectionError(self._com, error)
        elif error == QSerialPort.SerialPortError.ReadError:
            exception = SerialReadError(self._com, error)
        elif error == QSerialPort.SerialPortError.WriteError:
            exception = SerialWriteError(self._com, error)
        elif error == QSerialPort.SerialPortError.ResourceError:
            exception = SerialDisconnectedError(self._com, error, internal=True)
        else:
            exception = SerialUnknownError(self._com, error)

        self.close_connection()

        QTimer.singleShot(3000, self.scan_for_ports)

        self.error.emit(exception)
        raise exception

    def _port_filter(self, p: QSerialPort) -> bool:
        filters = [
            # p.portName().startswith("cu."),
            # "bluetooth" not in p.portName().lower()
        ]

        return all(filters)

    def _debug_ports(self, ports: List[QSerialPortInfo]) -> None:
        for p in ports:
            log.debug("-----------------------------")
            log.debug(f"name:         {p.portName()}")
            log.debug(f"manufacturer: {p.manufacturer()}")
            log.debug(f"productId:    {p.productIdentifier()}")
            log.debug(f"serialNumber: {p.serialNumber()}")
            log.debug(f"vendorId:     {p.vendorIdentifier()}")
            log.debug(f"systemLoc:    {p.systemLocation()}")

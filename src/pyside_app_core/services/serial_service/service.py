import logging
from typing import Generic, List

from PySide6.QtCore import QIODevice, QObject, QTimer, Signal
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo

from pyside_app_core import log
from pyside_app_core.errors.serial_errors import (
    SerialConnectionError,
    SerialDisconnectedError,
    SerialError,
    SerialReadError,
    SerialUnknownError,
    SerialWriteError,
)
from pyside_app_core.services.serial_service.types import (
    _TC,
    _TR,
    CanRegister,
    Encodable,
    PortFilter,
    SerialReader,
    TranscoderInterface,
)
from pyside_app_core.utils.time_ms import SECONDS

log.set_level(logging.DEBUG)


def _noop(ports):
    return ports


class SerialService(QObject, Generic[_TC, _TR]):
    ports = Signal(list)
    com_connect = Signal(QSerialPort)
    com_disconnect = Signal()
    data = Signal(object)
    error = Signal(Exception)

    def __init__(
        self, transcoder: type[TranscoderInterface[_TC, _TR]], parent: QObject
    ):
        super(SerialService, self).__init__(parent=parent)

        self._port_filter: PortFilter = _noop

        self._transcoder = transcoder
        self._com: QSerialPort | None = None
        self._buffer = bytearray()

    def _new_com(
        self, port_info: QSerialPortInfo
    ) -> tuple[QSerialPort, QSerialPort.SerialPortError | None]:
        com = QSerialPort(port_info, parent=self)
        com.setBaudRate(QSerialPort.BaudRate.Baud115200)
        open_ok = com.open(QIODevice.OpenModeFlag.ReadWrite)

        return com, None if open_ok else com.error()

    def set_port_filter(self, func: PortFilter):
        self._port_filter = func

    def open_connection(self, port_info: QSerialPortInfo) -> bool:
        self.close_connection()

        self._com, error = self._new_com(port_info)
        if error:
            self._on_error(error)
            return False

        self._com.readyRead.connect(self._on_data)
        self._com.errorOccurred.connect(self._on_error)

        self.com_connect.emit(self._com)

        return True

    def register_reader(self, reader: SerialReader) -> None:
        self.com_connect[QSerialPort].connect(reader.handle_serial_connect)
        self.com_disconnect.connect(reader.handle_serial_disconnect)
        self.ports.connect(reader.handle_serial_ports)
        self.data.connect(reader.handle_serial_data)
        self.error.connect(reader.handle_serial_error)
        reader.refresh_ports.connect(self.scan_for_ports)

    def link(self, *can_register: CanRegister):
        for item in can_register:
            item.bind_serial_service(self)

    def scan_for_ports(self) -> None:
        ports = QSerialPortInfo.availablePorts()

        self._debug_ports(ports)
        log.debug("sending ports...")

        self.ports.emit([p for p in ports if self._port_filter(p)])

    def send_data(self, data: Encodable) -> None:
        log.debug(f"sending data: {data}")

        if not self._com:
            log.debug("com port not connected")
            return

        self._com.write(self._transcoder.encode(data))

    def close_connection(self) -> None:
        if not self._com:
            return

        self.com_disconnect.emit()

        try:
            self._com.errorOccurred.disconnect()
            self._com.readyRead.disconnect()
        except Exception as e:
            log.exception(e)
            pass

        if self._com and self._com.isOpen():
            self._com.flush()
            self._com.close()

        self._com.deleteLater()
        self._com = None

    def deleteLater(self) -> None:
        self.close_connection()
        super().deleteLater()

    def _on_data(self, *args, **kwargs) -> None:
        if not self._com:
            return

        self._buffer.extend(bytearray(self._com.readAll()))

        chunks, remainder = self._transcoder.process_buffer(self._buffer)

        for chunk in chunks:
            try:
                result = self._transcoder.decode(chunk)
                log.debug(f"received data: {result}")
                self.data.emit(result)
            except Exception as e:
                log.exception(e)
                self.error.emit(e)

            self._buffer.clear()
            if remainder is not None:
                self._buffer.extend(remainder)

    def _on_error(self, error: QSerialPort.SerialPortError | None) -> None:
        exception: SerialError

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

        QTimer.singleShot(3 * SECONDS, self.scan_for_ports)

        self.error.emit(exception)
        raise exception

    def _debug_ports(self, ports: List[QSerialPortInfo]) -> None:
        for p in ports:
            log.debug("-----------------------------")
            log.debug(f"name:         {p.portName()}")
            log.debug(f"manufacturer: {p.manufacturer()}")
            log.debug(f"productId:    {p.productIdentifier()}")
            log.debug(f"serialNumber: {p.serialNumber()}")
            log.debug(f"vendorId:     {p.vendorIdentifier()}")
            log.debug(f"systemLoc:    {p.systemLocation()}")

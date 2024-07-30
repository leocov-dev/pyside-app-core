from typing import cast

from PySide6.QtCore import QIODevice, QObject, Signal
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
    Encodable,
    PortFilter,
    SerialReader,
    TranscoderInterface,
)


def _noop(ports: list[QSerialPortInfo]) -> list[QSerialPortInfo]:
    return ports


class SerialService(QObject):
    com_ports = Signal(list)
    com_connect = Signal(QSerialPort)
    com_disconnect = Signal()
    com_data = Signal(object)
    com_error = Signal(Exception)

    DEBUG = True

    def __init__(self, transcoder: type[TranscoderInterface], parent: QObject):
        super().__init__(parent=parent)

        self._port_filter: PortFilter = _noop

        self._transcoder: type[TranscoderInterface] = transcoder
        self._com: QSerialPort | None = None
        self._buffer = bytearray()

    @property
    def is_connected(self) -> bool:
        return self._com is not None and self._com.isOpen()

    def _new_com(self, port_info: QSerialPortInfo) -> tuple[QSerialPort, QSerialPort.SerialPortError | None]:
        com = QSerialPort(port_info, parent=self)
        com.setBaudRate(QSerialPort.BaudRate.Baud115200)
        open_ok = com.open(QIODevice.OpenModeFlag.ReadWrite)

        return com, None if open_ok else com.error()

    def set_port_filter(self, func: PortFilter) -> None:
        self._port_filter = func

    def open_connection(self, port_info: QSerialPortInfo | None) -> bool:
        if port_info is None:
            return False

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
        if self.DEBUG:
            log.debug(f"Registering reader {reader}")
        self.com_connect.connect(reader.handle_serial_connect)
        self.com_disconnect.connect(reader.handle_serial_disconnect)
        self.com_ports.connect(reader.handle_serial_ports)
        self.com_data.connect(reader.handle_serial_data)
        self.com_error.connect(reader.handle_serial_error)

    def scan_for_ports(self) -> None:
        log.debug("Scanning for ports...")
        ports = QSerialPortInfo.availablePorts()

        self._debug_ports(ports)

        filtered_ports = self._port_filter(ports)

        if self.DEBUG:
            log.debug(f"Sending ports: {[p.portName() for p in filtered_ports]}")

        self.com_ports.emit(filtered_ports)

    def send_data(self, data: Encodable) -> None:
        """send data to the connected port"""
        if self.DEBUG:
            log.debug(f"sending data: {data}")

        if not self._com:
            log.warning("can't send data, com port not connected")
            return

        self._com.write(self._transcoder.encode(data))

    def close_connection(self) -> None:
        if not self._com:
            return

        self.com_disconnect.emit()

        try:
            self._com.errorOccurred.disconnect()
            self._com.readyRead.disconnect()
        except Exception as e:  # noqa: BLE001
            log.exception(e)

        if self._com and self._com.isOpen():
            self._com.flush()
            self._com.close()

        self._com.deleteLater()
        self._com = None

    def deleteLater(self) -> None:
        self.close_connection()
        super().deleteLater()

    def _on_data(self, *_: object, **__: object) -> None:
        if not self._com:
            return

        raw = self._com.readAll()
        if self.DEBUG:
            log.debug(f"serial data: {raw!r}")
        self._buffer.extend(cast(bytearray, raw))

        chunks, remainder = self._transcoder.process_buffer(self._buffer)

        for chunk in chunks:
            try:
                result = self._transcoder.decode(chunk)
                if self.DEBUG:
                    log.debug(f"transcoded chunk: {result}")
                self.com_data.emit(result)
            except Exception as e:  # noqa: BLE001
                log.exception(e)
                self.com_error.emit(e)

            self._buffer.clear()
            if remainder is not None:
                self._buffer.extend(remainder)

    def _on_error(self, error: QSerialPort.SerialPortError | None) -> None:
        if self.DEBUG:
            log.debug(f"serial error: {error}")

        exception: SerialError

        if error is None or error == QSerialPort.SerialPortError.NoError:
            return
        if error == QSerialPort.SerialPortError.OpenError:
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

        # QTimer.singleShot(3 * SECONDS, self.scan_for_ports)

        self.com_error.emit(exception)
        raise exception

    def _debug_ports(self, ports: list[QSerialPortInfo]) -> None:
        if not self.DEBUG:
            return

        for p in ports:
            log.debug("-----------------------------")
            log.debug(f"name:         {p.portName()}")
            log.debug(f"manufacturer: {p.manufacturer()}")
            log.debug(f"productId:    {p.productIdentifier()}")
            log.debug(f"serialNumber: {p.serialNumber()}")
            log.debug(f"vendorId:     {p.vendorIdentifier()}")
            log.debug(f"systemLoc:    {p.systemLocation()}")

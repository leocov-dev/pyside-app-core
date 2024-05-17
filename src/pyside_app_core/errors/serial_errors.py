from PySide6 import QtSerialPort

from pyside_app_core.errors.basic_errors import CoreError


class SerialError(CoreError):
    def __init__(
        self,
        port: QtSerialPort.QSerialPort | None,
        error: QtSerialPort.QSerialPort.SerialPortError,
        *,
        internal: bool = False,
    ):
        if port:
            msg = f"Serial error{f' {error} ' if error else ' '}on port: {port.portName()}"
        else:
            msg = "Serial port not configured"
        super().__init__(msg, internal=internal)


class SerialUnknownError(SerialError):
    """something went wrong"""


class SerialConnectionError(SerialError):
    """a connection error occurred"""


class SerialReadError(SerialError):
    """a data read error occurred"""


class SerialWriteError(SerialError):
    """a data write error occurred"""


class SerialDisconnectedError(SerialError):
    """connection was broken"""

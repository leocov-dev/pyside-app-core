from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from pyside_app_core import log


class ConnectionManager(QtWidgets.QWidget):
    refresh_ports = Signal()
    request_connect = Signal(QSerialPortInfo)
    request_disconnect = Signal()

    def __init__(self, parent: QtWidgets.QWidget):
        super(ConnectionManager, self).__init__(parent=parent)

        _ly = QtWidgets.QVBoxLayout()
        _ly.setSpacing(0)
        _ly.setContentsMargins(5, 5, 5, 5)
        self.setLayout(_ly)

        _ly_list = QtWidgets.QHBoxLayout()
        _ly.addLayout(_ly_list)

        _ly_actions = QtWidgets.QHBoxLayout()
        _ly.addLayout(_ly_actions)

        self._refresh_btn = QtWidgets.QPushButton(
            icon=QtGui.QIcon(":/std/icons/reload"),
            parent=self,
        )
        self._refresh_btn.setContentsMargins(0, 0, 0, 0)
        self._refresh_btn.setToolTip(self.tr("Refresh Device List"))
        _ly_list.addWidget(self._refresh_btn)

        self._port_list = QtWidgets.QComboBox(self)
        self._port_list.setPlaceholderText(self.tr("Choose A Device"))
        _ly_list.addWidget(self._port_list, stretch=9)

        # ------------------------------------------------------------------------------\
        self._refresh_btn.clicked.connect(self._request_port_refresh)
        self._port_list.currentIndexChanged.connect(self._on_port_selected)

    @Slot()
    def handle_serial_connect(self, com: QSerialPort) -> None:
        pass

    @Slot()
    def handle_serial_disconnect(self) -> None:
        pass

    @Slot()
    def handle_serial_ports(self, ports: list[QSerialPortInfo]) -> None:
        self.setEnabled(True)
        self._port_list.clear()

        for port in ports:
            name = port.portName()

            self._port_list.addItem(name, port)

    @Slot()
    def handle_serial_data(self, data: object) -> None:
        pass

    @Slot()
    def handle_serial_error(self, error: Exception) -> None:
        pass

    def _request_port_refresh(self):
        log.debug("Requesting Port Refresh")
        self.setDisabled(True)
        self.refresh_ports.emit()

    def _on_port_selected(self, index: int):
        port = self._port_list.itemData(index, Qt.ItemDataRole.UserRole)
        log.debug(f"Port Selected: {port}")

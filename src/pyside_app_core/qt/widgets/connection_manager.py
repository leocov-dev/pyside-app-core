from typing import cast

from PySide6.QtCore import QSize, Qt, QTimer, Signal, Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from pyside_app_core import log
from pyside_app_core.qt.widgets.core_icon import CoreIcon
from pyside_app_core.qt.widgets.settings_mixin import SettingsMixin
from pyside_app_core.utils.time_ms import SECONDS


class ConnectionManager(SettingsMixin, QWidget):
    refresh_ports = Signal()
    request_connect = Signal(QSerialPortInfo)
    request_disconnect = Signal()

    SIZE = QSize(30, 30)
    ICON_SIZE = QSize(20, 20)

    def __init__(
        self,
        *,
        remember_last_connection: bool = False,
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)

        self._remember_last_connection = remember_last_connection

        _ly = QVBoxLayout()
        _ly.setSpacing(0)
        _ly.setContentsMargins(5, 5, 5, 5)
        self.setLayout(_ly)

        _ly_list = QHBoxLayout()
        _ly_list.setSpacing(5)
        _ly.addLayout(_ly_list)

        _ly_actions = QHBoxLayout()
        _ly.addLayout(_ly_actions)

        # -------
        # refresh button
        self._refresh_btn = QPushButton(
            icon=CoreIcon(":/core/iconoir/refresh-circle.svg"),
            text="",
            parent=self,
        )
        self._refresh_btn.setFixedSize(self.SIZE)
        self._refresh_btn.setIconSize(self.ICON_SIZE)
        self._refresh_btn.setContentsMargins(0, 0, 0, 0)
        self._refresh_btn.setToolTip("Refresh Device List")
        _ly_list.addWidget(self._refresh_btn)

        # -------
        # port selection list
        self._port_list = QComboBox(self)
        self._port_list.setPlaceholderText("Choose A Device")
        self._port_list.setFixedHeight(self.SIZE.height())
        _ly_list.addWidget(self._port_list, stretch=9)

        # --------
        # connect/disconnect button
        self._connect_btn = QPushButton(
            icon=CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
            text="",
            parent=self,
        )
        self._connect_btn.setCheckable(True)
        self._connect_btn.setFixedSize(self.SIZE)
        self._connect_btn.setIconSize(self.ICON_SIZE)
        self._connect_btn.setContentsMargins(0, 0, 0, 0)
        self._connect_btn.setToolTip("Refresh Device List")
        _ly_list.addWidget(self._connect_btn)

        # ------------------------------------------------------------------------------
        # signals
        self._refresh_btn.clicked.connect(self.request_port_refresh)
        self._port_list.currentIndexChanged.connect(self._on_port_selected)

    @property
    def current_port(self) -> QSerialPortInfo | None:
        return cast(
            QSerialPortInfo | None,
            self._port_list.currentData(Qt.ItemDataRole.UserRole),
        )

    @Slot()
    def handle_serial_connect(self, com: QSerialPort) -> None:
        log.debug(f"Connected to serial port {com.portName()}")

    @Slot()
    def handle_serial_disconnect(self) -> None:
        log.debug("Com port disconnected")
        self.request_port_refresh()

    @Slot()
    def handle_serial_ports(self, ports: list[QSerialPortInfo]) -> None:
        self.setEnabled(True)
        self._port_list.clear()

        for port in ports:
            name = port.portName()
            log.debug(f"Adding port {name}")

            self._port_list.addItem(name, port)

    @Slot()
    def handle_serial_data(self, data: object) -> None:
        log.debug(f"Received data: {data}")

    @Slot()
    def handle_serial_error(self, error: Exception) -> None:
        pass

    def request_port_refresh(self) -> None:
        log.debug("Requesting Port Refresh")
        self.setDisabled(True)
        QTimer.singleShot(1 * SECONDS, self.refresh_ports.emit)

    def _on_port_selected(self, index: int) -> None:
        port = self._port_list.itemData(index, Qt.ItemDataRole.UserRole)
        log.debug(f"Port Selected: {port}")
        self.request_connect.emit(port)

    def _format_port_name(self, port: QSerialPortInfo) -> str:
        name: str = port.portName()
        extra = ""
        if mfc := port.manufacturer():
            prod_id = port.productIdentifier()
            extra = f"{mfc}/{prod_id}" if prod_id else mfc

        return f"{name} ({extra})" if extra else name

    def _store_state(self) -> None:
        if not self._remember_last_connection:
            return

        if self.current_port and self.current_port.serialNumber():
            self._settings.setValue("last_port_serial", self.current_port.serialNumber())

    def _restore_state(self) -> None:
        if not self._remember_last_connection:
            return None

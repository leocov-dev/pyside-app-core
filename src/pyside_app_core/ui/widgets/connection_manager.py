from collections.abc import Callable
from typing import NamedTuple, cast

from PySide6.QtCore import QRect, QSize, Qt, QTimer, Signal, Slot
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QPalette, QStandardItem, QStandardItemModel
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from pyside_app_core import log
from pyside_app_core.mixin.settings_mixin import SettingsMixin
from pyside_app_core.ui.widgets.core_icon import CoreIcon
from pyside_app_core.utils.time_ms import SECONDS


class PortData(NamedTuple):
    display_name: str
    board: str


PortDataMapper = Callable[[QSerialPortInfo], PortData]


def _default_port_data_mapper(port_info: QSerialPortInfo) -> PortData:
    return PortData(port_info.systemLocation(), "unknown:unknown")


class ConnectionManager(SettingsMixin, QWidget):
    refresh_ports = Signal()
    request_connect = Signal(QSerialPortInfo)
    request_disconnect = Signal()
    port_changed = Signal(QSerialPortInfo, str)

    SIZE = QSize(30, 30)
    ICON_SIZE = QSize(20, 20)

    def __init__(
        self,
        autoconnect: bool = False,  # noqa: FBT002
        port_data_mapper: PortDataMapper = _default_port_data_mapper,
        remember_last_connection: bool = False,  # noqa: FBT002
        parent: QWidget | None = None,
    ):
        super().__init__(parent=parent)

        # autoconnect will automatically connect to a port the first time the app is opened
        # if there is only one port
        self._autoconnect = autoconnect
        self._autoconnect_done = False

        self._port_data_mapper = port_data_mapper

        # remember last connection will connect to the same port from the last session the first
        # time the app is opened (if possible)
        self._remember_last_connection = remember_last_connection
        self._last_port_serial: str | None = None

        _ly = QVBoxLayout()
        _ly.setSpacing(0)
        _ly.setContentsMargins(0, 0, 0, 0)
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
        # activity indicator
        self._activity = _ActivityIndicator(parent=self)
        self._activity.setFixedSize(self.ICON_SIZE)
        _ly_list.addWidget(self._activity)

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
                ":/core/iconoir/ev-plug-xmark.svg",
                ":/core/iconoir/ev-plug-charging.svg",
            ),
            text="Connect",
            parent=self,
        )
        self._connect_btn.setDisabled(True)
        self._connect_btn.setCheckable(True)
        self._connect_btn.setFixedHeight(self.SIZE.height())
        self._connect_btn.setIconSize(self.ICON_SIZE)
        self._connect_btn.setContentsMargins(0, 0, 0, 0)
        self._connect_btn.setToolTip("Connect to device")
        _ly_list.addWidget(self._connect_btn)

        # ------------------------------------------------------------------------------
        # signals
        self._refresh_btn.clicked.connect(self.request_port_refresh)
        self._port_list.currentIndexChanged.connect(self._on_port_selected)
        self._connect_btn.toggled.connect(self._update_connection_btn_text)
        # use clicked not toggled since it only registers on user action
        self._connect_btn.clicked.connect(self.request_connection_change)

    @property
    def current_port(self) -> QSerialPortInfo | None:
        return cast(
            QSerialPortInfo | None,
            self._port_list.currentData(Qt.ItemDataRole.UserRole),
        )

    @Slot()
    def handle_serial_connect(self, com: QSerialPort) -> None:
        log.debug(f"Connected to serial port {com.portName()}")
        self._connect_btn.setChecked(True)

    @Slot()
    def handle_serial_disconnect(self) -> None:
        log.debug("Com port disconnected")
        # self.request_port_refresh()

    @Slot()
    def handle_serial_ports(self, ports: list[QSerialPortInfo]) -> None:
        self.setEnabled(True)
        self._port_list.clear()

        remembered_index = -1

        model = QStandardItemModel(parent=self)

        for i, port in enumerate(ports):
            log.debug(f"Adding port {port.systemLocation()}")

            name, board = self._port_data_mapper(port)

            li = QStandardItem(name)
            li.setData(port, Qt.ItemDataRole.UserRole)
            li.setData(board, Qt.ItemDataRole.UserRole + 1)
            model.appendRow(li)

            if self._remember_last_connection and self._last_port_serial == port.serialNumber():
                remembered_index = i

        self._port_list.setModel(model)

        if remembered_index >= 0:
            # clear it out so only happens first time
            self._last_port_serial = None
            # also disable autoconnect
            self._autoconnect_done = True

            self._port_list.setCurrentIndex(remembered_index)
            self.request_connection_change(True)
        elif self._autoconnect and not self._autoconnect_done and len(ports) == 1:
            # mark done so it only happens first time
            self._autoconnect_done = True
            self._port_list.setCurrentIndex(0)
            self.request_connection_change(True)

    @Slot()
    def handle_serial_data(self, _: object) -> None:
        self._activity.tick()

    @Slot()
    def handle_serial_error(self, error: Exception) -> None:
        pass

    def request_port_refresh(self) -> None:
        self.setDisabled(True)
        self._connect_btn.setChecked(False)
        QTimer.singleShot(int(0.5 * SECONDS), self.refresh_ports.emit)

    def request_connection_change(self, connect: bool) -> None:
        if not self.current_port:
            return

        if connect:
            self.request_connect.emit(self.current_port)
        else:
            self.request_disconnect.emit()

    def _on_port_selected(self, index: int) -> None:
        self._connect_btn.setDisabled(index < 0)

        if index < 0:
            self.port_changed.emit(None, "")
            return

        port = cast(QSerialPortInfo, self._port_list.itemData(index, Qt.ItemDataRole.UserRole))
        board = cast(str, self._port_list.itemData(index, Qt.ItemDataRole.UserRole + 1))
        log.debug(f"Port Selected: {port.portName()}, {board}")
        self.port_changed.emit(port, board)

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
            self._settings.setValue(
                "last_port_serial",
                self.current_port.serialNumber(),
            )

    def _restore_state(self) -> None:
        if self._remember_last_connection:
            self._last_port_serial = self.get_setting("last_port_serial", None, str)

    def _update_connection_btn_text(self, checked: bool) -> None:
        self._connect_btn.setText("Disconnect" if checked else "Connect")
        self._connect_btn.setToolTip("Disconnect active port" if checked else "Connect to port")


class _ActivityIndicator(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._lit = False
        self._ticking = False
        self._on = QColor(20, 175, 20)
        self._off = QColor(100, 100, 100)

    def tick(self) -> None:
        if self._ticking:
            return

        self._lit = True
        self.repaint()
        self._ticking = True

        def _off() -> None:
            self._ticking = False
            self._lit = False
            self.repaint()

        # this timeout will be the max speed for ticking,
        # ticks faster than this will not be painted
        QTimer.singleShot(int(0.05 * SECONDS), _off)

    def paintEvent(self, e: QPaintEvent) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        smaller = min(self.rect().width(), self.rect().height())
        smaller = int(smaller * 0.8)
        square = QRect(0, 0, smaller, smaller)

        square.moveCenter(self.rect().center())

        p.setPen(QColor(self.palette().color(QPalette.ColorRole.Dark)))
        p.setBrush(self._on if self._lit else self._off)

        p.drawEllipse(square)

        p.end()
        e.accept()

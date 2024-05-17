"""
Adapted from:
https://gis.stackexchange.com/questions/350148/qcombobox-multiple-selection-pyqt5
"""

from collections.abc import Generator
from typing import Generic, TypeVar, cast

from PySide6.QtCore import (
    QEvent,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    QSize,
    Qt,
    QTimerEvent,
    Signal,
)
from PySide6.QtGui import (
    QFontMetrics,
    QMouseEvent,
    QResizeEvent,
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QComboBox,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.qt.widgets.settings_mixin import SettingsMixin

DT = TypeVar("DT")


class MultiComboBox(ObjectNameMixin, SettingsMixin, QComboBox, Generic[DT]):
    """a combo box of checkable items.
    The selected options will be listed as text in the combo box line.
    The first option is a show/hide all option.
    """

    class Delegate(QStyledItemDelegate):
        def sizeHint(
            self,
            option: QStyleOptionViewItem,
            index: QModelIndex | QPersistentModelIndex,
        ) -> QSize:
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    selectionChanged = Signal(list)

    def __init__(
        self,
        placeholder_text: str,
        all_text: str = "Show/Hide All",
        parent: QWidget | None = None,
        *args: object,
        **kwargs: object,
    ) -> None:
        super(MultiComboBox, self).__init__(parent=parent, *args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setPlaceholderText(placeholder_text)

        # Use custom delegate
        self.setItemDelegate(MultiComboBox.Delegate())

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        self.addItem(all_text, isChecked=True)

        self.model().itemChanged.connect(self._update_selection)
        self.model().dataChanged.connect(self._update_text)
        self.model().dataChanged.connect(self._emit_current_data)

    def model(self) -> QStandardItemModel:
        return cast(QStandardItemModel, super().model())

    def _emit_current_data(self) -> None:
        self.selectionChanged.emit(self.currentData())

    def _update_selection(self, item: QStandardItem) -> None:
        if item.index().row() == 0:
            # update on the show/hide all case
            state = item.checkState()
            self.model().layoutAboutToBeChanged.emit()
            for item in self.modelItems():
                item.setCheckState(state)
            self.model().layoutChanged.emit()

    def resizeEvent(self, event: QResizeEvent) -> None:
        # Recompute text to elide as needed
        self._update_text()
        super().resizeEvent(event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.lineEdit():
            if event.type() == QEvent.Type.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if watched == self.view().viewport():
            if (
                isinstance(event, QMouseEvent)
                and event.type() == QEvent.Type.MouseButtonRelease
            ):
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)
                return True
        return False

    def showPopup(self) -> None:
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self) -> None:
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self._update_text()

    def timerEvent(self, event: QTimerEvent) -> None:
        # After timeout, kill timer, and re-enable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def _update_text(self) -> None:
        texts = []
        for item in self.modelItems():
            if item.checkState() == Qt.CheckState.Checked:
                texts.append(item.text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        text = metrics.elidedText(
            text, Qt.TextElideMode.ElideRight, self.lineEdit().width()
        )
        self.lineEdit().setText(text)

    def addItem(  # type:ignore[override]
        self,
        text: str,
        userData: DT | None = None,
        isChecked: bool = False,
        **kwargs: object,
    ) -> None:
        item = QStandardItem()
        item.setText(text)
        if userData is None:
            item.setData(text, Qt.ItemDataRole.UserRole)
        else:
            item.setData(userData, Qt.ItemDataRole.UserRole)

        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if isChecked else Qt.CheckState.Unchecked
        )

        self.model().appendRow(item)

    def addItems(  # type:ignore[override]
        self,
        texts: list[str],
        dataList: list[DT] | None = None,
        allChecked: bool = False,
    ) -> None:
        for i, text in enumerate(texts):
            try:
                data = (dataList or [])[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data, isChecked=allChecked)

    def currentData(self, role: Qt.ItemDataRole = Qt.ItemDataRole.UserRole) -> list[DT]:  # type: ignore[override]
        res = []
        for item in self.modelItems():
            if item.checkState() == Qt.CheckState.Checked:
                res.append(item.data(role))
        return res

    def currentOptions(self) -> list[tuple[str, DT]]:
        res = []
        for item in self.modelItems():
            if item.checkState() == Qt.CheckState.Checked:
                res.append((item.text(), item.data(Qt.ItemDataRole.UserRole)))
        return res

    def modelItems(self) -> Generator[QStandardItem, None, None]:
        for i in range(1, self.model().rowCount()):
            yield self.model().item(i)

    def _restore_state(self) -> None:
        options = cast(list[str], self._settings.value(f"{self.obj_name}_options"))
        if not options:
            return

        for item in self.modelItems():
            state = (
                Qt.CheckState.Checked
                if item.text() in options
                else Qt.CheckState.Unchecked
            )
            item.setCheckState(state)

    def _store_state(self) -> None:
        self._settings.setValue(
            f"{self.obj_name}_options", [n for n, _ in self.currentOptions()]
        )

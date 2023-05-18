from enum import IntEnum, StrEnum
from typing import Dict, Generic, NamedTuple, TypeVar

from pyqtgraph import SpinBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core import log


class ParamConfig(NamedTuple):
    label: str
    init_val: int | float
    min_val: int | float
    max_val: int | float
    step: int | float
    unit: str | None


PT = TypeVar("PT", StrEnum, IntEnum)


class ParamListWidget(ObjectNameMixin, Generic[PT], QWidget):
    param_changed = Signal()

    OBJECT_NAME = "ParamListWidget"
    TITLE: str

    def __init__(self, param_config: Dict[PT, ParamConfig], parent: QWidget):
        super(ParamListWidget, self).__init__(parent=parent)

        self._params: Dict[StrEnum | IntEnum, SpinBox] = {
            key: self._gen_widget(val) for key, val in param_config.items()
        }

        _layout = QVBoxLayout()
        _layout.setContentsMargins(8, 5, 0, 0)
        _layout.setSpacing(15)
        self.setLayout(_layout)

        _title = QLabel(self.TITLE)
        _title.setObjectName(f"{self.obj_name}_TITLE")
        _layout.addWidget(_title)

        self._form_layout = QVBoxLayout()
        self._form_layout.setContentsMargins(0, 0, 0, 10)
        self._form_layout.setSpacing(5)
        _layout.addLayout(self._form_layout)

        for k, w in self._params.items():
            w.valueChanged.connect(lambda _, x=k: self._on_value_changed(x))
            _row = QHBoxLayout()
            _row.setContentsMargins(0, 0, 0, 0)
            _row.setSpacing(0)
            self._form_layout.addLayout(_row)

            _label = QLabel(param_config[k].label)
            _label.setObjectName(f"{self.obj_name}_HEADING")
            _label.setMinimumHeight(30)
            _label.setSizePolicy(
                QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
            )

            _row.addWidget(_label, alignment=Qt.AlignmentFlag.AlignVCenter)
            _row.addWidget(w, alignment=Qt.AlignmentFlag.AlignVCenter)

    def _on_value_changed(self, kind: StrEnum | IntEnum):
        log.debug(kind.name, self._params[kind].value())

    def _gen_widget(self, config: ParamConfig) -> SpinBox:
        sb = SpinBox(parent=self)
        sb.setMinimumHeight(30)
        sb.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )

        sb.setMinimum(config.min_val)
        sb.setMaximum(config.max_val)
        sb.setValue(config.init_val)
        sb.setSingleStep(config.step)

        if config.unit:
            sb.setOpts(suffix=config.unit, siPrefix=True)

        return sb

    @property
    def values(self) -> Dict[StrEnum | IntEnum, int | float]:
        return {k: v.value() for k, v in self._params.items()}

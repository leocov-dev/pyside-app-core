from typing import TypeVar, Union

from pyqtgraph import SpinBox
from PySide6.QtWidgets import QDoubleSpinBox, QSpinBox, QWidget

T = TypeVar("T", int, float)

ParamSpinBoxType = Union[QDoubleSpinBox, QSpinBox]


def param_spin_box(
    value: T, vmin: T, vmax: T, parent: QWidget, step=1, suffix=""
) -> ParamSpinBoxType:
    if type(value) == float:
        sb = SpinBox(parent)
        sb.setMinimum(vmin)
        sb.setMaximum(vmax)
        sb.setValue(value)
        sb.setSingleStep(step)
    else:
        sb = SpinBox(parent)
        sb.setMinimum(vmin)
        sb.setMaximum(vmax)
        sb.setValue(value)
        sb.setSingleStep(step)

    if suffix:
        sb.setOpts(suffix=suffix, siPrefix=True)

    return sb

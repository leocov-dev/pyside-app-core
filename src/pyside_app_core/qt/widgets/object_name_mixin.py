from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


class ObjectNameMixin:
    def __init__(self, *args, **kwargs):
        super(ObjectNameMixin, self).__init__(*args, **kwargs)

        if isinstance(self, QWidget):
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        obj_name = self.__class__.__name__
        if hasattr(self, "OBJECT_NAME"):
            obj_name = self.OBJECT_NAME.replace(" ", "_")

        self.setObjectName(obj_name)

    @property
    def obj_name(self):
        return self.objectName()

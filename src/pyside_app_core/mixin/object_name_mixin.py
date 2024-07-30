from typing import cast

from PySide6.QtCore import QObject


class ObjectNameMixin:
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)

        if hasattr(self, "OBJECT_NAME"):
            obj_name = str(self.OBJECT_NAME).replace(" ", "_").strip()
        else:
            obj_name = self.__class__.__name__

        cast(QObject, self).setObjectName(obj_name)

    @property
    def object_name(self) -> str:
        return cast(QObject, self).objectName()

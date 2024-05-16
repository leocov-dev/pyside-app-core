from PySide6.QtCore import QFile, QTextStream


def load_text_file(file_url: str) -> str:
    qfile = QFile(file_url)
    qfile.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    ts = QTextStream(qfile)
    return ts.readAll()

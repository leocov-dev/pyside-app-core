from pathlib import Path

from PySide6 import QtGui
from PySide6.QtCore import Qt


def generate_project_icon(icon_target: Path, letter: str) -> Path:
    letter = letter.upper()[0]

    q_app = QtGui.QGuiApplication()

    pix = QtGui.QPixmap(256, 256)
    pix.fill(QtGui.QColor(0, 0, 0, 0))

    paint = QtGui.QPainter()
    paint.begin(pix)

    paint.setRenderHints(
        QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing
    )

    pen = QtGui.QPen()
    pen.setColor(QtGui.QColor(0, 0, 0))
    pen.setWidth(10)
    paint.setPen(pen)

    paint.setBrush(QtGui.QColor(220, 220, 220))

    paint.drawRoundedRect(pix.rect().adjusted(6, 6, -6, -6), 60, 60)

    # TODO: support more than one letter and calculate the optimum size

    font = q_app.font()
    font.setBold(True)
    font.setPointSize(230)
    paint.setFont(font)

    paint.drawText(
        pix.rect(),
        Qt.AlignmentFlag.AlignCenter,
        letter,
    )

    paint.end()

    pix.save(str(icon_target))

    q_app.quit()

    return icon_target


if __name__ == '__main__':
    generate_project_icon(
        Path(__file__).parent / "Test.png",
        "TC"
    )

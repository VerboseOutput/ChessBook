import sys

import hichess

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile, QTextStream
from PySide2.QtGui import QPixmap

from context import resources

# QMainWindow provides the framework for building an applications top level interface
class Window(QMainWindow):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        # Setup hichess widget
        self.boardWidget = hichess.BoardWidget()
        self.boardWidget.accessibleSides = hichess.BOTH_SIDES
        self.boardWidget.dragAndDrop = True

        # background image
        self.boardWidget.setBoardPixmap(defaultPixmap=QPixmap(":/images/chessboard.png"),
                                        flippedPixmap=QPixmap(":/images/flipped_chessboard.png"))

        # qss
        qss = QFile(":/styles/styles.css")
        if qss.open(QFile.ReadOnly):
            textStream = QTextStream(qss)
            self.boardWidget.setStyleSheet(textStream.readAll())
        else:
            print(f"failed to open{qss.fileName()}")

        self.setCentralWidget(self.boardWidget)

        self.setWindowTitle("ChessBook")
        self.resize(width, height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    scale = 0.8
    window = Window(int(width * scale), int(height * scale))

    sys.exit(app.exec_())  # Start main event loop
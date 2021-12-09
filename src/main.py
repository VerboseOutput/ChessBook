import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PySide2.QtCore import QFile, QTextStream
from PySide2.QtGui import QPixmap

from context import resources
from square_board import SquareBoardWidget
import hichess

# QMainWindow provides the framework for building an applications top level interface
class Window(QMainWindow):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        # Setup hichess widget
        self.boardWidget = SquareBoardWidget()
        board = self.boardWidget.board()

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.boardWidget, 1, 1)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

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
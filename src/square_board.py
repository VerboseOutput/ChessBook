from PySide2.QtWidgets import QGridLayout, QWidget, QSizePolicy
from PySide2.QtCore import QFile, QTextStream
from PySide2.QtGui import QPixmap, QPainter, QColor

from hichess.hichess import BoardWidget

class SquareBoardWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # create hichess board widget
        board = BoardWidget(self)
        self.boardWidget = board

        # resize it to be square and centered within its parent widget
        # this needs to happen before setting the board pixmap
        board.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        boardSize = self._boardSize(self.rect().width(), self.rect().height())
        board.setFixedSize(boardSize, boardSize)

        # setup board and pieces
        board.setBoardPixmap(defaultPixmap=QPixmap(":/images/chessboard.png"),
                            flippedPixmap=QPixmap(":/images/flipped_chessboard.png"))
        qss = QFile(":/styles/styles.css")
        if qss.open(QFile.ReadOnly):
            textStream = QTextStream(qss)
            board.setStyleSheet(textStream.readAll())
        else:
            print(f"failed to open{qss.fileName()}")

    def board(self):
        return self.boardWidget

    def _resizeBoard(self, size):
        self.boardWidget.setFixedSize(size, size)

    def _boardSize(self, width, height):
        return width if width < height else height

    def paintEvent(self, event):
        painter = QPainter(self)
        # TODO: fill entire widget area with red for debugging
        #       remove
        painter.fillRect(self.rect(), QColor(64, 0, 0)) 

    def resizeEvent(self, event):
        widgetSize = event.size()
        boardSize = self._boardSize(widgetSize.width(), widgetSize.height())
        self._resizeBoard(boardSize)

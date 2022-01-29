from PySide2.QtWidgets import QWidget, QSizePolicy
from PySide2.QtCore import QFile, QTextStream, QRect
from PySide2.QtGui import QPixmap

from hichess.hichess import BoardWidget

class SquareBoardWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # create hichess board widget, with this widget as its parent
        board = BoardWidget(self)

        # resize it to be square and centered within its parent widget
        # this needs to happen before setting the board pixmap
        boardGeo = self._boardGeo(self.rect().width(), self.rect().height())
        board.setGeometry(boardGeo)

        # setup board and pieces
        board.setBoardPixmap(defaultPixmap=QPixmap(":/images/chessboard.png"),
                            flippedPixmap=QPixmap(":/images/flipped_chessboard.png"))
        qss = QFile(":/styles/styles.css")
        if qss.open(QFile.ReadOnly):
            textStream = QTextStream(qss)
            board.setStyleSheet(textStream.readAll())
        else:
            print(f"failed to open{qss.fileName()}")

        self._boardWidget = board

    @property
    def board_widget(self):
        return self._boardWidget

    def peek_move(self):
        return self._boardWidget.board.peek()

    def resizeEvent(self, event):
        widgetSize = event.size()
        boardGeo = self._boardGeo(widgetSize.width(), widgetSize.height())
        
        self.board_widget.setGeometry(boardGeo)

    def _boardGeo(self, widgetWidth, widgetHeight) -> QRect:
        """maximize board size while maintaining square aspect ratio and centering"""

        boardSize = widgetWidth if widgetWidth < widgetHeight else widgetHeight
        boardX = (widgetWidth - boardSize) / 2  
        boardY = (widgetHeight - boardSize) / 2

        return QRect(boardX, boardY, boardSize, boardSize)

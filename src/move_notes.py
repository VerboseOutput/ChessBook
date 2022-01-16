from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PySide2.QtGui import QPainter, QColor, QFont, QFontDatabase
from chess import pgn, WHITE, BLACK

from chess_line import LineWidget

class MoveNotesWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.curr_line = LineWidget()
        self.layout.addWidget(self.curr_line)
        

        self.setLayout(self.layout)

    def add_move(self, node: pgn.ChildNode):
        self.curr_line.add_move(node)



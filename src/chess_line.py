from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PySide2.QtGui import QPainter, QColor, QFont, QPalette
from chess import pgn, WHITE, BLACK

from flow_layout import FlowLayout

class MoveWidget(QLabel):
    def __init__(self, font_size: int) -> None:
        super().__init__()

        self.setText("")
        self.node = None

        font = QFont("Monaco", font_size, QFont.Bold)
        self.setFont(font)

        self.selected = False

        self.setAutoFillBackground(True)
        self.default_background = self.palette().color(self.backgroundRole())
        self.selected_color = QColor(100, 100, 100)

    def set_node(self, node: pgn.ChildNode):
        self.node = node
        self.setText(self.node.san())

    def is_set(self) -> bool:
        return self.node is not None

    def select(self):
        self.selected = True
        self.set_background(self.selected_color)

    def deselect(self):
        self.selected = False
        self.set_background(self.default_background)

    def set_background(self, color):
        pal = self.palette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)

class TurnWidget(QWidget):
    def __init__(self, moveNum: int, font_size: int) -> None:
        super().__init__()

        self.white_move = MoveWidget(font_size)
        self.black_move = MoveWidget(font_size)

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(8)
        
        move_num = QLabel(str(moveNum) + ".")
        move_num.setStyleSheet("QLabel { color : #C0C0C0; }")
        font = QFont("Monaco", font_size)
        move_num.setFont(font)
        
        layout.addWidget(move_num)
        
        layout.addWidget(self.white_move)
        layout.addWidget(self.black_move)
        
        self.setLayout(layout)

    def setWhiteMove(self, node: pgn.ChildNode):
        self.white_move.set_node(node)
        return self.white_move

    def setBlackMove(self, node: pgn.ChildNode):
        if not self.white_move.is_set():
            self.white_move.setText("...")
        self.black_move.set_node(node)
        return self.black_move
class LineWidget(QWidget):
    def __init__(self, turn_num: int = 1, font_size: int = 16) -> None:
        super().__init__()

        self.font_size = font_size

        self.turn_number = turn_num
        self.curr_turn = None
        self.layout = FlowLayout()

        self.setLayout(self.layout)

    def add_move(self, node: pgn.ChildNode)  -> MoveWidget:
        if self.curr_turn is None:
            self.curr_turn = TurnWidget(self.turn_number, self.font_size)
            self.layout.addWidget(self.curr_turn)

        if node.turn() is BLACK: # means this node was WHITE'S move
            move = self.curr_turn.setWhiteMove(node)
        else:
            move = self.curr_turn.setBlackMove(node)
            self.turn_number += 1
            self.curr_turn = None

        return move
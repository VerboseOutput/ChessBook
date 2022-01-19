from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PySide2.QtGui import QPainter, QColor, QFont, QFontDatabase
from chess import pgn, WHITE, BLACK

from flow_layout import FlowLayout

class MoveWidget(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setText("")
        self.node = None

        font = QFont("Monaco", 16, QFont.Bold)
        self.setFont(font)

    def set_node(self, node: pgn.ChildNode):
        self.node = node
        self.setText(self.node.san())

    def is_set(self) -> bool:
        return self.node is not None
class TurnWidget(QWidget):
    def __init__(self, moveNum: int) -> None:
        super().__init__()

        self.white_move = MoveWidget()
        self.black_move = MoveWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(8)
        
        move_num = QLabel(str(moveNum) + ".")
        move_num.setStyleSheet("QLabel { color : #C0C0C0; }")
        font = QFont("Monaco", 16)
        move_num.setFont(font)
        
        layout.addWidget(move_num)
        
        layout.addWidget(self.white_move)
        layout.addWidget(self.black_move)
        
        self.setLayout(layout)

    def setWhiteMove(self, node: pgn.ChildNode):
        self.white_move.set_node(node)

    def setBlackMove(self, node: pgn.ChildNode):
        if not self.white_move.is_set():
            self.white_move.setText("...")
        self.black_move.set_node(node)


    
class LineWidget(QWidget):
    def __init__(self, turn_num: int = 1) -> None:
        super().__init__()

        self.turn_number = turn_num
        self.curr_turn = None
        self.layout = FlowLayout()

        self.setLayout(self.layout)

    def add_move(self, node: pgn.ChildNode):
        if self.curr_turn is None:
            self.curr_turn = TurnWidget(self.turn_number)
            self.layout.addWidget(self.curr_turn)

        if node.turn() is BLACK: # means this node was WHITE'S move
            self.curr_turn.setWhiteMove(node)
        else:
            self.curr_turn.setBlackMove(node)
            self.turn_number += 1
            self.curr_turn = None
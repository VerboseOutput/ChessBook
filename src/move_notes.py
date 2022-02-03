from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QGridLayout
from PySide2.QtGui import QPainter, QColor, QFont, QFontDatabase
from PySide2.QtCore import Qt, Slot, Signal
from chess import pgn, WHITE, BLACK

from chess_line import LineWidget, MoveWidget

class MoveNotesWidget(QWidget):
    update_position = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.curr_line = LineWidget()
        self.layout.addWidget(self.curr_line)
        
        self.setLayout(self.layout)

        self.active_move = None

    def add_move(self, node: pgn.ChildNode):
        # if no other move already exists
        new_move_widget = self.curr_line.add_move(node)
        self.set_active(new_move_widget)

        new_move_widget.clicked.connect(self.on_move_selected)
        

    @Slot(MoveWidget)
    def on_move_selected(self, move_widget: MoveWidget):
        
        self.update_position.emit(move_widget.node.board().fen())

        self.set_active(move_widget)
    
    def set_active(self, move_widget: MoveWidget) -> None:
        if self.active_move is not None:
            self.active_move.deselect()

        self.active_move = move_widget
        move_widget.select()



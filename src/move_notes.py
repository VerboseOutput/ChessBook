from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from chess import pgn, WHITE, BLACK

from flow_layout import FlowLayout

class MoveWidget(QLabel):
    WIDTH = 5
    def __init__(self) -> None:
        super().__init__()

        self.setText("")
        self.node = None

    def setText(self, text: str):
        text = text.ljust(MoveWidget.WIDTH)
        super().setText(text)

    def setNode(self, node: pgn.ChildNode):
        self.node = node
        self.setText(self.node.san())

    def isSet(self) -> bool:
        return self.node is not None

class TurnWidget(QWidget):
    def __init__(self, moveNum: int) -> None:
        super().__init__()

        self.whiteMove = MoveWidget()
        self.blackMove = MoveWidget()

        layout = QHBoxLayout()
        layout.addWidget(QLabel(str(moveNum) + ". "))
        layout.addWidget(self.whiteMove)
        layout.addWidget(self.blackMove)
        
        self.setLayout(layout)

    def setWhiteMove(self, node: pgn.ChildNode):
        self.whiteMove.setNode(node)

    def setBlackMove(self, node: pgn.ChildNode):
        if not self.whiteMove.isSet():
            self.whiteMove.setText("...")
        self.blackMove.setNode(node)
    

class MoveNotesWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.turnNumber = 1
        self.currTurn = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


    def addMove(self, node: pgn.ChildNode):
        if node.turn() is BLACK: # means this node was WHITE'S move
            self.currTurn = TurnWidget(self.turnNumber)
            self.currTurn.setWhiteMove(node)

            self.layout.addWidget(self.currTurn)

        else:
            self.currTurn.setBlackMove(node)
            self.turnNumber += 1



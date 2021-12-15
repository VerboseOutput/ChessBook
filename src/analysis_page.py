from PySide2.QtWidgets import QWidget, QLabel, QGridLayout
from PySide2.QtCore import Qt
import hichess
from chess import pgn
import chess

from square_board import SquareBoardWidget


class AnalysisPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # games are represented by a tree of pgn.GameNodes, with the root node
        # being a special subclass of GameNode, Game, with some additional header info
        #
        # each node can return a chess.Board representation of the current state
        # add a new move after the current one using add_variation()
        self.gameRoot = pgn.Game()
        self.currentNode = self.gameRoot

        # Setup Board Widget
        self.sqBoardWidget = SquareBoardWidget()

        boardWidget = self.sqBoardWidget.boardWidget
        boardWidget.accessibleSides = hichess.BOTH_SIDES
        boardWidget.dragAndDrop = True

        boardWidget.moveMade.connect(self._onMoveMade)

        # placeholder labels for future widgets
        self.moveNotes = QLabel("TODO: move notes")
        self.lines = QLabel("TODO: engine lines")

        # layout the page's widgets
        layout = QGridLayout()
        layout.addWidget(self.sqBoardWidget, 0, 0)
        layout.addWidget(self.moveNotes, 0, 1, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.lines, 1, 0,Qt.AlignHCenter | Qt.AlignTop)

        self.setLayout(layout)

    def _onMoveMade(self, move: str):
        move = self.sqBoardWidget.peekMove()
        self.currentNode.add_variation(move)
        self.currentNode = self.currentNode.next()
        print(self.currentNode.board())

    
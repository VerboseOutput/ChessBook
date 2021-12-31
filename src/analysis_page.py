from PySide2.QtWidgets import QWidget, QLabel, QGridLayout
from PySide2.QtCore import Qt
import hichess
from chess import pgn
import chess
from move_notes import MoveNotesWidget

from square_board import SquareBoardWidget


class AnalysisPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # games are represented by a tree of pgn.GameNodes (an abstract base class), with the root node
        # being a special subclass of GameNode, Game, with some additional header info
        # all nodes after the root will be of "ChildNode" type
        #
        # each node can return a chess.Board representation of the current state
        # add a new move after the current one using add_variation()
        self.gameNode = pgn.Game()

        # Setup Board Widget
        self.sqBoardWidget = SquareBoardWidget()

        boardWidget = self.sqBoardWidget.boardWidget
        boardWidget.accessibleSides = hichess.BOTH_SIDES
        boardWidget.dragAndDrop = True

        boardWidget.moveMade.connect(self._onMoveMade)

        # placeholder labels for future widgets
        self.moveNotes = MoveNotesWidget()
        self.lines = QLabel("TODO: engine lines")

        # layout the page's widgets
        layout = QGridLayout()
        layout.addWidget(self.sqBoardWidget, 0, 0)
        layout.addWidget(self.moveNotes, 0, 1, 2, 1, Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.lines, 1, 0,Qt.AlignHCenter | Qt.AlignTop)

        self.setLayout(layout)

    def _onMoveMade(self, _):
        """handle user move input via the board widget"""

        # get the latest move from our board widget
        move = self.sqBoardWidget.peekMove()

        # update our source of truth for the game state
        self.gameNode = self.gameNode.add_variation(move)

        # update our notes with the latest move
        self.moveNotes.addMove(self.gameNode)



    
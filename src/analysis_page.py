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
        self.game_node = pgn.Game()

        # Setup Board Widget
        self.sq_board_widget = SquareBoardWidget()

        board_widget = self.sq_board_widget.board_widget
        board_widget.accessibleSides = hichess.BOTH_SIDES
        board_widget.dragAndDrop = True

        board_widget.moveMade.connect(self._on_move_made)

        # placeholder labels for future widgets
        self.move_notes = MoveNotesWidget()
        self.lines = QLabel("TODO: engine lines")

        # layout the page's widgets
        layout = QGridLayout()
        layout.addWidget(self.sq_board_widget, 0, 0)
        layout.addWidget(self.move_notes, 0, 1, 2, 1)
        layout.addWidget(self.lines, 1, 0, Qt.AlignHCenter | Qt.AlignTop)

        self.setLayout(layout)

    def _on_move_made(self, _):
        """handle user move input via the board widget"""

        # get the latest move from our board widget
        move = self.sq_board_widget.peek_move()

        # update our source of truth for the game state
        self.game_node = self.game_node.add_variation(move)

        # update our notes with the latest move
        self.move_notes.add_move(self.game_node)



    
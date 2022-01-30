from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea
from PySide2.QtCore import Qt
import hichess
from chess import pgn
from chess import engine
from chess_line import MoveWidget
from engine_evaluation import EngineEvaluationWidget
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
        self.activeMove = None

        # Setup Board Widget
        self.sq_board_widget = SquareBoardWidget()

        board_widget = self.sq_board_widget.board_widget
        board_widget.accessibleSides = hichess.BOTH_SIDES
        board_widget.dragAndDrop = True

        board_widget.moveMade.connect(self._on_move_made)

        # Setup Engine for position evaluation
        self.engine_evaluation = EngineEvaluationWidget()
       
       # Setup notes and move recorder
        self.move_notes = MoveNotesWidget()
    
        # layout the page's widgets
        layout = QGridLayout()

        # left side
        layout.addWidget(self.sq_board_widget, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.engine_evaluation)
        layout.addWidget(scroll, 1, 0)

        # right side
        layout.addWidget(self.move_notes, 0, 1, 2, 1)
        
        # set size policy
        layout.setColumnStretch(0,1)
        layout.setColumnStretch(1,2)

        # minimum size of board widget is 1/2 window height
        # so that might affect any "rowStretch" settings you put here
        # in unexpected ways

        self.setLayout(layout)

    def _on_move_made(self, _):
        """handle user move input via the board widget"""

        # update our source of truth for the game state
        move = self.sq_board_widget.peek_move()
        self.game_node = self.game_node.add_variation(move)

        # send the new position to the engine
        self.engine_evaluation.evaluate(self.game_node)

        # update our notes with the latest move
        new_move_widget = self.move_notes.add_move(self.game_node)
        self.set_active(new_move_widget)
        

    def resizeEvent(self, event):
        widgetSize = event.size()

        # required to keep the engine analysis lines from growing to take up
        # the entire area. would love a better way to do this though
        self.sq_board_widget.setMinimumSize(0, widgetSize.height() * 0.5)

    def set_active(self, move_widget: MoveWidget) -> None:
        if self.activeMove is not None:
            self.activeMove.deselect()

        self.activeMove = move_widget
        move_widget.select()
    
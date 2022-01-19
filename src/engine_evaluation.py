from PySide2.QtWidgets import QWidget, QLabel, QGridLayout
from chess import engine
import chess

from chess_line import LineWidget

class EngineEvaluationWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # requires stockfish to be installed on your system such that it can be
        # called from the command line using the cmd: "stockfish"
        self.engine = engine.SimpleEngine.popen_uci("stockfish")
        self.score = QLabel("0")
        self.main_line = LineWidget()

        self.layout = QGridLayout()
        self.layout.addWidget(self.score, 0, 0)
        self.layout.addWidget(self.main_line, 0, 1)
        self.setLayout(self.layout)

    def analyse(self, game_node):
        info = self.engine.analyse(game_node.board(), engine.Limit(depth=20))

        relative_score = info["score"]
        white_score = relative_score.white() # always get the score from white's point of view
        # TODO check for mate
        self.score.setText(str(white_score.score())) 

        # replace the current line widget
        dummy = QWidget()
        self.layout.replaceWidget(self.main_line, dummy)
        self.main_line = LineWidget()
        self.layout.replaceWidget(dummy, self.main_line)

        eval_node = game_node
        pv = info["pv"]
        for move in pv:
            eval_node = eval_node.add_variation(move)
            self.main_line.add_move(eval_node)



    
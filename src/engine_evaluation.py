import threading
import asyncio
import concurrent

from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QScrollArea, QSizePolicy
from PySide2.QtCore import Signal, Slot
from chess import engine
import chess
from rich import print


from chess_line import LineWidget

class EngineEvaluationWidget(QWidget):
    evaluation = Signal(chess.Board, engine.PovScore, list, int)
    variation_count = 3

    def __init__(self) -> None:
        super().__init__()

        self.evaluation.connect(self.update_evaluation)

        self.event_loop = asyncio.new_event_loop()
        self.engine_thread = threading.Thread(target=self.start_background_loop, args=(self.event_loop,), daemon=True)
        self.engine_thread.start()

        self.analyze_task = None
        self.engine = None
        self.start_engine()

        self.layout = QGridLayout()

        self.score = [QLabel("0") for x in range(EngineEvaluationWidget.variation_count)]
        self.variation = [LineWidget() for x in range(EngineEvaluationWidget.variation_count)]

        for index in range(EngineEvaluationWidget.variation_count):
            self.layout.addWidget(self.score[index], index, 0)
            self.layout.addWidget(self.variation[index], index, 1)

        # set size policy
        self.layout.setColumnStretch(1,1) # give more room to the lines than the scores

        self.setLayout(self.layout)

    def start_background_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def start_engine(self):
        try:
            task = asyncio.run_coroutine_threadsafe(chess.engine.popen_uci("stockfish"), self.event_loop)
            timeout = 5 # seconds
            _, self.engine = task.result(timeout)
        except concurrent.futures.TimeoutError:
            print('The coroutine took too long, cancelling the task...')
            task.cancel()
        except Exception as exc:
            print(f'The coroutine raised an exception: {exc!r}')
        else:
            print(f'The coroutine returned: {type(self.engine)}')

    def evaluate(self, board):
        if self.analyze_task is not None:
            self.analyze_task.cancel()
               
        self.analyze_task = asyncio.run_coroutine_threadsafe(self.analyze(board), self.event_loop)        

    async def analyze(self, board):
        # wait on event which sets the position to be analyzed
        with await self.engine.analysis(board, multipv=3) as analysis:
            async for info in analysis:
                relative_score = info.get("score")
                pv = info.get("pv")
                multipv = info.get("multipv") # 1 indexed based, NOT 0

                if (relative_score is not None and 
                    pv is not None):
                    self.evaluation.emit(board, relative_score, pv, multipv)
        
    @Slot(chess.Board, engine.PovScore, list, int)
    def update_evaluation(self, board, relative_score, pv, multipv):
        v_index = multipv - 1 # convert 1 indexed to 0 indexed

        white_score = relative_score.white() # always get the score from white's point of view
        self.score[v_index].setText(str(white_score.score() / 100.0)) # convert from centipawns to pawns

        # replace the current line widget
        font_size = 12
        turn_num = board.fullmove_number
        dummy = QWidget()
        self.layout.replaceWidget(self.variation[v_index], dummy)
        self.variation[v_index] = LineWidget(turn_num, font_size)
        self.layout.replaceWidget(dummy, self.variation[v_index])

        node = chess.pgn.Game()
        node.setup(board)
        for move in pv:
            node = node.add_variation(move)
            self.variation[v_index].add_move(node)


    
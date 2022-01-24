import threading
import asyncio
import concurrent

from PySide2.QtWidgets import QWidget, QLabel, QGridLayout
from PySide2.QtCore import Signal, Slot
from chess import engine
import chess
from rich import print


from chess_line import LineWidget

class EngineEvaluationWidget(QWidget):
    evaluation = Signal(chess.pgn.ChildNode, engine.PovScore, list, int)
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

        self.score = [0] * EngineEvaluationWidget.variation_count
        self.variation = [LineWidget()] * EngineEvaluationWidget.variation_count
        for index in range(EngineEvaluationWidget.variation_count):
            self.score[index] = QLabel("0")
            self.variation[index] = LineWidget()

            self.layout.addWidget(self.score[index], index, 0)
            self.layout.addWidget(self.variation[index], index, 1)

        #self.layout.setColumnStretch(1,1) # give more room to the lines than the scores

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

    def evaluate(self, game_node):
        if self.analyze_task is not None:
            self.analyze_task.cancel()
               
        self.analyze_task = asyncio.run_coroutine_threadsafe(self.analyze(game_node), self.event_loop)        

    async def analyze(self, game_node):
        board = game_node.board()
        # wait on event which sets the position to be analyzed
        with await self.engine.analysis(board, multipv=3) as analysis:
            curr_pv_len = [0] * EngineEvaluationWidget.variation_count
            async for info in analysis:
                relative_score = info.get("score")
                pv = info.get("pv")
                multipv = info.get("multipv") # 1 indexed based, NOT 0

                if (relative_score is not None and 
                    pv is not None and
                    len(pv) >= curr_pv_len[multipv-1]):

                    curr_pv_len[multipv-1] = len(pv)
                    self.evaluation.emit(game_node, relative_score, pv, multipv)
        
    @Slot(chess.pgn.ChildNode, engine.PovScore, list, int)
    def update_evaluation(self, game_node, relative_score, pv, multipv):
        v_index = multipv - 1

        white_score = relative_score.white() # always get the score from white's point of view
        self.score[v_index].setText(str(white_score.score())) 

        # replace the current line widget
        dummy = QWidget()
        self.layout.replaceWidget(self.variation[v_index], dummy)
        self.variation[v_index] = LineWidget()
        self.layout.replaceWidget(dummy, self.variation[v_index])

        eval_node = game_node
        for move in pv:
            eval_node = eval_node.add_variation(move)
            self.variation[v_index].add_move(eval_node)


    
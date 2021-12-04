"""  A module defining classes for a custom board widget
"""
import os
from collections import defaultdict

from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtSvg import QSvgRenderer

class Square():
    """ A class representing an individual square of a chess board """
    def __init__(self, file: str, rank: str, loc: QRect, color: QColor) -> None:
        super().__init__()

        self.file = file
        self.rank = rank
        self.loc = loc
        self.color = color
        self.piece = None

    def paint(self, painter: QPainter):
        painter.fillRect(self.loc, self.color)

    

class Board(QOpenGLWidget):
    """ A widget representing a chess board"""

    def __init__(self) -> None:
        super().__init__()

        wp_renderer = QSvgRenderer("assets/white_pawn.svg")

    def getBoardRect(self) -> QRect:
        """ Determine size and location of board given widget size"""
        
        # widget size
        rect = self.rect()
        total_width = rect.width()
        total_height = rect.height()

        # create a square board within our widget with size divisible by eight
        # so that every square has the same number of pixels
        board_size = total_width if (total_width < total_height) else total_height
        board_margin = board_size % 8
        board_size = board_size - board_margin
        board_rect = QRect(
            (total_width - board_size) / 2,     # x
            (total_height - board_size) / 2,    # y
            board_size,                         # width
            board_size)                         # height

        return board_rect

    def getSquares(self, board_rect: QRect) -> defaultdict(dict):
        """ create dictionary collection of all board squares"""

        squares = defaultdict(dict)
        light_square = False
        light_color = QColor(200, 200, 200)
        dark_color = QColor(60, 120, 60)

        square_size = board_rect.width() / 8
        for col, file in enumerate('abcdefgh'):
            light_square = not light_square
            for row, rank in enumerate('87654321'): # notice we're counting down b/c origin is top left
                loc = QRect(
                    board_rect.x() + (col * square_size),    # x
                    board_rect.y() + (row * square_size),    # y 
                    square_size,                             # width
                    square_size                              # height
                )
                color = light_color if light_square else dark_color
                light_square = not light_square

                square = Square(file, rank, loc, color)
                squares[file][rank] = square
        
        return squares
        
    def paintEvent(self, event):
        painter = QPainter(self)
        # TODO: fill entire widget area with red for debugging
        #       remove
        painter.fillRect(self.rect(), QColor(64, 0, 0)) 

        board_rect = self.getBoardRect()
        # TODO: fill chess board area with blue for debugging
        #       remove
        painter.fillRect(board_rect, QColor(0, 0, 64)) # TODO: for debugging, remove

        squares = self.getSquares(board_rect)
        for file in squares.values():
            for square in file.values(): 
                square.paint(painter)
            
        
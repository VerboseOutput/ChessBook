import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide2.QtGui import QGuiApplication

from context import resources
from analysis_page import AnalysisPage
from flow_layout import FlowLayout


# QMainWindow provides the framework for building an applications top level interface
class Window(QMainWindow):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        # Setup hichess widget
        self.analysis_page = AnalysisPage()

        self.setCentralWidget(self.analysis_page)

        self.setWindowTitle("ChessBook")
        self.resize(width, height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen_resolution = QGuiApplication.primaryScreen().availableGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    scale = 0.8
    window = Window(int(width * scale), int(height * scale))

    sys.exit(app.exec_())  # Start main event loop
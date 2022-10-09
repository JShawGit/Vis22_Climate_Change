from application.widgets import ExampleWidget
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import altair as alt
import numpy as np
import sys
import os


class Application(QApplication):
    def __init__(self, args):
        super(Application, self).__init__(args)
        self.setQuitOnLastWindowClosed(True)


class MainWindow(QMainWindow):
    """
        https://blog.devgenius.io/building-your-own-python-data-visualization-desktop-app-f82dd1f9b2ed
        https://doc.qt.io/qtforpython/tutorials/datavisualize/plot_datapoints.html
    """
    def __init__(self, config):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.icon = QIcon(config['icon'])

        self.init_window(config)
        self.show()

    def init_window(self, config):
        # Adds the configuration options to the main window
        self.setWindowTitle(config['title'])
        self.setFixedSize(QSize(config['size'][0], config['size'][1]))
        self.setWindowIcon(self.icon)

        # Add the default window widgets
        widget = ExampleWidget()
        self.setCentralWidget(widget)



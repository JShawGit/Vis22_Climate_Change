from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import sys
import os


class Window(QMainWindow):
    """
        https://blog.devgenius.io/building-your-own-python-data-visualization-desktop-app-f82dd1f9b2ed
        https://doc.qt.io/qtforpython/tutorials/datavisualize/plot_datapoints.html
    """
    def __init__(self, args):
        super().__init__(args)

from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import altair as alt
import pandas as pd
import numpy as np
import random


class ExampleWidget(PlotWidget):
    """
        https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
        https://pyqtgraph.readthedocs.io/en/latest/getting_started/how_to_use.html
    """
    def __init__(self):
        super().__init__()
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.plot(hour, temperature)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from mpl_toolkits.basemap import Basemap, shiftgrid
from processing.data_processor import get_data
from matplotlib.figure import Figure
from matplotlib import colors as c
from pyqtgraph import PlotWidget
from processing import read_data
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
import plotly.express as px
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import altair as alt
import pandas as pd
import numpy as np
import matplotlib
import random

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

"""
    https://www.pythonguis.com/tutorials/plotting-pyqtgraph/
    https://pyqtgraph.readthedocs.io/en/latest/getting_started/how_to_use.html
    https://plotly.com/python/bubble-maps/
    https://annefou.github.io/metos_python/04-plotting/
"""

matplotlib.use('Qt5Agg')


class ExamplePrecipWidget:
    def __init__(self):
        data = get_data(to_get={'precip': 'precip/precip.V1.0.*.nc'})['precip']
        lats = data.variables['lat'][:]
        lons = data.variables['lon'][:]
        precips = data.variables['precip'][0, :, :]

        fig = plt.figure(figsize=[12, 15])
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title('Precip test', fontsize=14)

        map = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c', ax=ax)

        map.drawcoastlines()
        map.fillcontinents(color='#ffe2ab')
        map.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
        map.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])

        llons, llats = np.meshgrid(lons, lats)
        x, y = map(llons, llats)
        cmap = c.ListedColormap(['#00004c', '#000080', '#0000b3', '#0000e6', '#0026ff', '#004cff',
                                 '#0073ff', '#0099ff', '#00c0ff', '#00d900', '#33f3ff', '#73ffff', '#c0ffff',
                                 (0, 0, 0, 0),
                                 '#ffff00', '#ffe600', '#ffcc00', '#ffb300', '#ff9900', '#ff8000', '#ff6600',
                                 '#ff4c00', '#ff2600', '#e60000', '#b30000', '#800000', '#4c0000'])
        bounds = [-200, -100, -75, -50, -30, -25, -20, -15, -13, -11, -9, -7, -5, -3, 3, 5, 7, 9, 11, 13, 15, 20, 25, 30, 50, 75, 100, 200]
        norm = c.BoundaryNorm(bounds, ncolors=cmap.N)  # cmap.N gives the number of colors of your palette

        cs = map.contourf(x, y, precips, cmap=cmap, norm=norm, levels=bounds)
        fig.colorbar(cs, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds, ax=ax, orientation='horizontal')

        self.canvas = FigureCanvasTkAgg(fig, master=parent)
        self.canvas.draw()


class ExampleMapWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(ExampleMapWidget, self).__init__(fig)

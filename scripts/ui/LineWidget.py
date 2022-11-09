from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
import plotly.express as px
import pandas as pd


class Ui_LineWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 550)
        self.browser = QWebEngineView(self)
        self.make_plot()
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Plot Widget")

    def make_plot(self):
        df = px.data.gapminder(year=2007)
        fig = px.scatter(
            df, x="gdpPercap", y="lifeExp",
            color="continent", size="pop",
            template="simple_white", hover_name="country",
            size_max=60, log_x=True, height=600
        ).update_layout(hovermode=False)
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

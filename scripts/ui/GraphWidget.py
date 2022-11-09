
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.express as px
import pandas as pd
import plotly


class GraphWidget(QWebEngineView):
    def __init__(self):
        super(GraphWidget, self).__init__(parent=None)

        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')

        fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Magnitude', radius=10,
                            center=dict(lat=0, lon=180), zoom=0, hover_name="Date",
                            mapbox_style="stamen-terrain", height=600,
                           color_continuous_scale="magma")
        html = '<html><body>'
        html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        html += '</body></html>'

        self.setHtml(html)

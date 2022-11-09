from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QMainWindow
from processing.data_processor import *
from matplotlib import pyplot as plt
import cartopy.crs as ccrs



class Ui_MapWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(600, 550)
        self.browser = MapExample()
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Map Widget")

class MapExample(FigureCanvasQTAgg):
    def __init__(self):
        data = get_data(preprocessed='../data/preprocessed/precip', to_get={'precip': 'precip/precip.V1.0.2021.nc'})['precip']
        fig, axs = plt.subplots(ncols=1, subplot_kw={'projection': ccrs.NearsidePerspective(-90, 40, satellite_height=3000000)})
        axs = data.to_array().isel(time=0).plot(
            subplot_kws=dict(projection=ccrs.NearsidePerspective(-90, 40, satellite_height=3000000), facecolor="gray"),
            transform=ccrs.PlateCarree(),
        )
        axs.axes.set_global()
        axs.axes.coastlines()
        super(MapExample, self).__init__(fig)

        """
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
        fig = px.density_mapbox(
            df,
            lat='Latitude', lon='Longitude', z='Magnitude',
            radius=10, center=dict(lat=0, lon=180), zoom=0,
            hover_name="Date", mapbox_style="stamen-terrain",
            height=600, color_continuous_scale="magma"
        )
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        """

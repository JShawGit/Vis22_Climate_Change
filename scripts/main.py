from PyQt5 import QtWidgets
import sys

from ui.MainWindow import Ui_ClimateUI as UC
from ui.LineWidget import Ui_LineWidget as LW
from ui.MapWidget import Ui_MapWidget as MW

def main(config):
    app = QtWidgets.QApplication(sys.argv)
    main_window = UC()
    main_window.show()

    map = MW()
    map.show()
    line_graph = LW()
    line_graph.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    #download_data()
    config = '../config/app_configuration.json'
    main(config)

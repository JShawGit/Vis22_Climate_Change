from application.app import MainWindow, Application
from data_preprocessing import parser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


def window():
    config = parser.get_config('../config/app_configuration.json')['window_config']
    app = Application(sys.argv)
    main_window = MainWindow(config)
    app.exec_()


if __name__ == '__main__':
    window()

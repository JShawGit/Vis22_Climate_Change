from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_ClimateUI(QMainWindow):
    def __init__(self, parent=None, width=1161, height=648):
        super().__init__(parent)
        self.resize(width, height)
        self.setWindowTitle("ClimateUI")

        """ Main Window ------------------------------------- """
        self._create_main_menu()

        """ MDI Area ------------------------------------- """
        self._create_mdi()

        """ Status bar ------------------------------------- """
        self._create_status_bar()

        """ Menu bar ------------------------------------- """
        self._create_menu_bar()

        """ Color Options ------------------------------------- """
        self._create_color_options()

        """ Filter Options ------------------------------------- """
        self._create_filter_options()

        """ Central Widget ------------------------------------- """
        self.setCentralWidget(self.MainWindow)

    def _create_main_menu(self):
        # The main window of the program
        self.MainWindow = QtWidgets.QWidget()
        self.MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.MainWindow.setObjectName("Main Window")

        # The layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.MainWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")

    def _create_mdi(self):
        # The MDI area
        self.mdiArea = QtWidgets.QMdiArea(self.MainWindow)
        self.mdiArea.setObjectName("mdiArea")
        self.horizontalLayout.addWidget(self.mdiArea)

    def _create_status_bar(self):
        # The status bar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def _create_menu_bar(self):
        # The menu bar
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1161, 26))
        self.menubar.setObjectName("menubar")

        """ Change Data -------------------------------- """
        # 1. Change Data dialogue
        self.menuChange_Data = QtWidgets.QMenu(self.menubar)
        self.menuChange_Data.setObjectName("menuChange_Data")

        # 1a. Precipitation
        self.actionPrecipitation = QtWidgets.QAction()
        self.actionPrecipitation.setObjectName("actionPrecipitation")
        #self.actionPrecipitation.triggered[QtWidgets.QAction].connect(self._new_data_action)
        self.menuChange_Data.addAction(self.actionPrecipitation)

        # 2a. Temperature
        self.actionTemperature = QtWidgets.QAction()
        self.actionTemperature.setObjectName("actionTemperature")
        #self.actionTemperature.triggered[QtWidgets.QAction].connect(self._new_data_action)
        self.menuChange_Data.addAction(self.actionTemperature)

        # Set text
        self.menuChange_Data.setTitle("ClimateUI")
        self.actionTemperature.setText("Temperature")
        self.actionPrecipitation.setText("Precipitation")
        self.menubar.addAction(self.menuChange_Data.menuAction())

        """ New View -------------------------------- """
        # 2. New View dialogue
        self.menuNew_View = QtWidgets.QMenu(self.menubar)
        self.menuNew_View.setObjectName("menuNew_View")
        self.setMenuBar(self.menubar)

        # 2a. The map
        self.actionMap = QtWidgets.QAction()
        self.actionMap.setObjectName("actionMap")
        #self.actionPrecipitation.triggered[QtWidgets.QAction].connect(self._new_view_action)
        self.menuNew_View.addAction(self.actionMap)

        # 2b. The line graph
        self.actionLine_Graph = QtWidgets.QAction()
        self.actionLine_Graph.setObjectName("actionLine_Graph")
        #self.actionPrecipitation.triggered[QtWidgets.QAction].connect(self._new_view_action)
        self.menuNew_View.addAction(self.actionLine_Graph)

        # Set text
        self.actionMap.setText("Map")
        self.menuNew_View.setTitle("New View")
        self.actionLine_Graph.setText("Line Graph")
        self.menubar.addAction(self.menuNew_View.menuAction())

    def _create_color_options(self):
        self.ColorOptions = QtWidgets.QDockWidget()
        self.ColorOptions.setObjectName("ColorOptions")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.verticalLayout_4.addWidget(self.widget)
        self.verticalLayout.addWidget(self.groupBox)
        self.ColorOptions.setWidget(self.dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.ColorOptions)

        # Set text
        self.ColorOptions.setWindowTitle("Color Options")

    def _create_filter_options(self):
        self.FilterOptions = QtWidgets.QDockWidget()
        self.FilterOptions.setObjectName("FilterOptions")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.dockWidgetContents_2)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_2 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_3.addWidget(self.widget_2)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.FilterOptions.setWidget(self.dockWidgetContents_2)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.FilterOptions)

    #def menu_action(self, q):

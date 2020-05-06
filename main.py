
import PyQt5
from PyQt5 import QtWidgets, QtCore
from ui import SJCGuiMain
from sklearn_tools import NLTKUtils
from sklearn_tools.sklearn_extensions.NLTKUtils import *


if __name__ == '__main__':
    import sys

    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)



    if True:
        MainWindow = QtWidgets.QMainWindow()
        ui = SJCGuiMain()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
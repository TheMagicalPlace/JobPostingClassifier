

from PyQt5 import QtWidgets, QtCore
import ui as _ui

import sys

if __name__ == '__main__':

    MainWindow = QtWidgets.QMainWindow()
    ui = _ui.SJCGuiMain()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(_ui.ui_app.exec_())

""" The init file for the ui elements, also sets the UI scaling factor on import, this is used throughout
the UI to try to ensure proper scaling on every system. Kind of wonky with linux currently."""



__all__ = ['SJCGuiMain','SCALE_FACTOR','ui_app']

import sys
from PyQt5 import QtWidgets,QtCore
from ui.file_tree_setup import file_setup

def set_ui_scale():
    """Sets the universal UI scaling factor, should never be used outside the __init__.py file"""
    # TODO test on other OS and resolutions
    moniter_h = QtWidgets.QDesktopWidget().screenGeometry(-1).height()
    if sys.platform == 'win32':
        if moniter_h == 1080:
            scale = 1.0
        elif moniter_h == 1440:
            scale = 1.0
        else:
            scale = 1.0
    elif sys.platform == 'linux':
        if moniter_h == 1080:
            scale = 1.0
        elif moniter_h == 1440:
            scale = 1.23
        else:
            scale = 1.4
    elif sys.platform == 'darwin':
        if moniter_h == 1080:
            scale = 1.0
        elif moniter_h == 1440:
            scale = 1.25
        else:
            scale = 1.55
    return scale

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

ui_app = QtWidgets.QApplication(sys.argv)
SCALE_FACTOR = set_ui_scale()

ui_app.lastWindowClosed.connect(lambda  : ui_app.quit())
from ui.result_navigator import ResultsWindow as _ResultsWindow
from ui.train_select import TrainSelectWindow as _TrainSelectWindow
from ui.qt_gui import SJCGuiMain

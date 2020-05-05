
__all__ = ['SJCGuiMain','SCALE_FACTOR']
import sys
from PyQt5 import QtWidgets,QtCore
from ui.file_tree_setup import file_setup


def set_ui_scale():
    # TODO test on other OS and resolutions
    moniter_h = QtWidgets.QDesktopWidget().screenGeometry(-1).height()
    if sys.platform == 'win32':
        if moniter_h == 1080:
            scale = 0.8
        elif moniter_h == 1440:
            scale = 1.0
        else:
            scale = 1.25
    elif sys.platform == 'linux':
        if moniter_h == 1080:
            scale = 1.0
        elif moniter_h == 1440:
            scale = 1.25
        else:
            scale = 1.55
    elif sys.platform == 'darwin':
        if moniter_h == 1080:
            scale = 1.0
        elif moniter_h == 1440:
            scale = 1.25
        else:
            scale = 1.55
    return scale

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
__qtapp_core = QtWidgets.QApplication(sys.argv)
SCALE_FACTOR = set_ui_scale()


from ui.result_navigator import ResultsWindow as _ResultsWindow
from ui.train_select import TrainSelectWindow as _TrainSelectWindow
from ui.qt_gui import SJCGuiMain

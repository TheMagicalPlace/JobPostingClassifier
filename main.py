import multiprocessing



def main():
    import os
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtCore import QObject
    import ui as _ui
    import sklearn
    import sys
    os.environ['JOBLIB_MULTIPROCESSING'] = '0'
    _ui.file_setup()
    MainWindow = QtWidgets.QMainWindow()
    ui = _ui.SJCGuiMain()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(_ui.ui_app.exec_())



if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

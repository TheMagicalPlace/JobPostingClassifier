import multiprocessing



def main():
    import os
    from PyQt5 import QtWidgets
    from src import ui as _ui
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

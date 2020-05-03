# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'classifierguiup.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import PyQt5
import os,json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtCore import pyqtSlot,pyqtSignal
from scrapers import IndeedClient,LinkdinClient
from NBJobClassifier import ClassificationInterface,QWorkerCompatibleClassificationInterface
import sqlite3
from collections import defaultdict
from webdriver_handlers import DriverManagerChrome,DriverManagerFirefox
from train_select import *
from result_navigator import ResultsWindow

SCALE_FACTOR = 1.2


class WorkerSignals(QtCore.QObject):

    finished = pyqtSignal()

class WorkerGeneric(QtCore.QRunnable):

    def __init__(self,method,*args,**kwargs):
        super().__init__()
        self.method = method
        self.args =args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.method(*self.args,**self.kwargs)
        self.signals.finished.emit()




class SJCGuiMain(object):
    def __init__(self):
        self.ThreadPool = QtCore.QThreadPool()
    def __update_file_terms(self,file_term):
        with open(os.path.join(os.getcwd(), 'user_information', 'settings.json'), 'r+') as data:
            settings = json.loads(data.read())
            setdict = defaultdict(list, settings)

            if file_term not in setdict['file_terms']:
                setdict['file_terms'].append(file_term)
            file_terms = setdict['file_terms']
            data.seek(0)
            data.write(json.dumps(dict(setdict)))
        return file_terms

    def __toggle_other_tabs(self,state : bool,ignore=()):
        self.Classify.setEnabled(state)
        self.Search.setEnabled(state)
        self.SearchClassify.setEnabled(state)
        self.Train.setEnabled(state)
        self.Classify.setEnabled(state)
        for enabled in ignore:
            enabled.setEnabled(True)


    def __get_file_terms(self):
        with open(os.path.join(os.getcwd(), 'user_information', 'settings.json'), 'r') as data:
            terms = defaultdict(list,json.loads(data.read()))['file_terms']
        if 'None' not in  terms:
            terms = self.__update_file_terms('None')
        return terms

    def file_term_dropdown(self,dropdown):
        _translate = QtCore.QCoreApplication.translate
        for i,term in enumerate(self.__get_file_terms()):
            dropdown.addItem(term)

    def __setup_top_menu(self):

        # TODO add exception catching for invalid os or timeout
        def __download_chromedriver():
            self.dl_1_button.setEnabled(False)
            manager= DriverManagerChrome()
            worker = WorkerGeneric(manager.download_drivers)
            worker.signals.finished.connect(lambda : self.dl_1_button.setEnabled(True))
            self.ThreadPool.start(worker)
        def download_geckodriver():
            self.dl_2_button.setEnabled(False)
            manager = DriverManagerFirefox()
            worker = WorkerGeneric(manager.download_drivers)
            worker.signals.finished.connect(lambda : self.dl_2_button.setEnabled(True))
            self.ThreadPool.start(worker)

        def __send_usage_info():
            pass
        def __report_issue():
            pass
        def __exit():
            QtWidgets.qApp.exit()


        self.buttton_top_frame = QtWidgets.QFrame(self.centralwidget)
        self.buttton_top_frame.setGeometry(QtCore.QRect(int(340*SCALE_FACTOR), int(10*SCALE_FACTOR), int(541*SCALE_FACTOR), int(41*SCALE_FACTOR)))
        # color stuff
        if True:
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
                brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
                brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
                brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
                brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.buttton_top_frame.setPalette(palette)
        self.buttton_top_frame.setAutoFillBackground(True)
        self.buttton_top_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.buttton_top_frame.setObjectName("buttton_top_frame")
        self.report_issue_button = QtWidgets.QPushButton(self.buttton_top_frame)
        self.report_issue_button.setGeometry(QtCore.QRect(int(390*SCALE_FACTOR), int(10*SCALE_FACTOR), int(91*SCALE_FACTOR), int(23*SCALE_FACTOR)))
        self.report_issue_button.setObjectName("report_issue_button")
        self.usage_button = QtWidgets.QPushButton(self.buttton_top_frame)
        self.usage_button.setGeometry(QtCore.QRect(int(280*SCALE_FACTOR), int(10*SCALE_FACTOR), int(101*SCALE_FACTOR), int(23*SCALE_FACTOR)))
        self.usage_button.setObjectName("usage_button")
        self.dl_1_button = QtWidgets.QPushButton(self.buttton_top_frame)
        self.dl_1_button.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(131*SCALE_FACTOR), int(23*SCALE_FACTOR)))
        self.dl_1_button.setObjectName("dl_1_button")
        self.dl_2_button = QtWidgets.QPushButton(self.buttton_top_frame)
        self.dl_2_button.setGeometry(QtCore.QRect(int(150*SCALE_FACTOR), int(10*SCALE_FACTOR), int(121*SCALE_FACTOR), int(23*SCALE_FACTOR)))
        self.dl_2_button.setObjectName("dl_2_button")
        self.exit_button = QtWidgets.QPushButton(self.buttton_top_frame)
        self.exit_button.setGeometry(QtCore.QRect(int(490*SCALE_FACTOR), int(10*SCALE_FACTOR), int(41*SCALE_FACTOR), int(23*SCALE_FACTOR)))
        self.exit_button.setObjectName("exit_button")
        self.asthetic_top_frame = QtWidgets.QFrame(self.centralwidget)
        self.asthetic_top_frame.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(331*SCALE_FACTOR), int(21*SCALE_FACTOR)))
        if True:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.asthetic_top_frame.setPalette(palette)
        self.asthetic_top_frame.setAutoFillBackground(True)
        self.asthetic_top_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.asthetic_top_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.asthetic_top_frame.setObjectName("asthetic_top_frame")
        self.asthetic_top_frame_2 = QtWidgets.QFrame(self.asthetic_top_frame)
        self.asthetic_top_frame_2.setGeometry(QtCore.QRect(int(0*SCALE_FACTOR), int(0*SCALE_FACTOR), int(421*SCALE_FACTOR), int(21*SCALE_FACTOR)))
        if True:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.asthetic_top_frame_2.setPalette(palette)
        self.asthetic_top_frame_2.setAutoFillBackground(True)
        self.asthetic_top_frame_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.asthetic_top_frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.asthetic_top_frame_2.setObjectName("asthetic_top_frame_2")

        self.dl_1_button.clicked.connect(__download_chromedriver)
        self.dl_2_button.clicked.connect(download_geckodriver)
        self.usage_button.clicked.connect(__send_usage_info)
        self.report_issue_button.clicked.connect(__report_issue)
        self.exit_button.clicked.connect(__exit)

    def __setup_info_tab(self):
        self.Info = QtWidgets.QWidget()
        self.Info.setObjectName("Info")
        self.intro_cont = QtWidgets.QGroupBox(self.Info)
        self.intro_cont.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(871*SCALE_FACTOR), int(351*SCALE_FACTOR)))
        self.intro_cont.setTitle("")
        self.intro_cont.setObjectName("intro_cont")
        self.intro_info = QtWidgets.QTextBrowser(self.intro_cont)
        self.intro_info.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(851*SCALE_FACTOR), int(331*SCALE_FACTOR)))
        self.intro_info.setObjectName("intro_info")
        self.MainTab.addTab(self.Info, "")

    def __setup_search_tab(self):

        # conainer used to check if all required forms are filled
        # 1 - search term
        # 2 - No. of Jobs to Find
        # 3 - Location
        # 4 - Username, only required for linkedin
        # 5  -Pasword - only required for linkedin
        run_flag_container = {1:False,2:False,3:False,4:True,5:True}

        def __search_switch():
            if self.st_input.toPlainText():
                run_flag_container[1] = True
                __enable_run()
            else:
                run_flag_container[1] = False

        def __find_amt_switch():
            amt = self.no_jobs_input.toPlainText()
            try:
                amt = int(amt)
            except ValueError as e:
                print('input a number')
                run_flag_container[2] = False
            else:
                if amt:
                    run_flag_container[2] = True

                else:
                    run_flag_container[2] = False
            __enable_run()

        def __location_switch():
            if self.location_input.toPlainText():
                run_flag_container[3] = True
            else:
                run_flag_container[3] = False
            __enable_run()

        def __username_switch():
            if self.lk_username_in.toPlainText():
                run_flag_container[4] = True
            else:
                run_flag_container[4] = False
            __enable_run()

        def __password_switch():
            if self.lk_password_in.toPlainText():
                run_flag_container[5] = True
            else:
                run_flag_container[5] = False
            __enable_run()

        def __linkedin_forms_toggle():
            if self.jb_dropdown.currentText() == 'LinkedIn':
                self.linkedin_info_groupBox.setDisabled(False)
                run_flag_container[4] = False
                run_flag_container[5] = False
            else:
                self.linkedin_info_groupBox.setDisabled(True)
                run_flag_container[4] = True
                run_flag_container[5] = True
            __enable_run()

        def __enable_run():
            if all([_ for _ in run_flag_container.values()]):
                self.search_button.setDisabled(False)
            else:
                self.search_button.setDisabled(True)

        def __run_search():
            search_term = self.st_input.toPlainText()
            file_term = self.ft_input.currentText()
            location = self.location_input.toPlainText()
            jobs_to_find = int(self.no_jobs_input.toPlainText())
            self.__toggle_other_tabs(False,[self.Search,])
            # if no file term is given, set to search term
            if file_term == 'None':
                file_term = search_term
                self.__update_file_terms(file_term)

            terms = self.__get_file_terms()
            self.search_button.setEnabled(False)

            if self.jb_dropdown.currentText() == 'LinkedIn':
                username = self.lk_username_in.toPlainText()
                # TODO send password directly to scraper
                if self.lk_checkbox.isChecked():
                    pass
                    # TODO setup secure saving of linkedin info
                client= LinkdinClient(search_term=search_term,
                                      file_term=file_term,
                                      location=location,
                                      jobs_to_find=jobs_to_find)
                worker = WorkerGeneric(client,[username,self.lk_password_in.toPlainText()])
                self.ThreadPool.start(worker)
            elif self.jb_dropdown.currentText() == 'Indeed':
                client = IndeedClient(search_term=search_term,
                                      file_term=file_term,
                                      location=location,
                                      jobs_to_find=jobs_to_find)
                worker = WorkerGeneric(client)
                self.ThreadPool.start(worker)
            worker.signals.finished.connect(lambda : self.search_button.setEnabled(True))
            worker.signals.finished.connect(lambda :  self.__toggle_other_tabs(True))

        self.Search = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Search.sizePolicy().hasHeightForWidth())
        self.Search.setSizePolicy(sizePolicy)
        self.Search.setObjectName("Search")
        self.search_cont = QtWidgets.QGroupBox(self.Search)
        self.search_cont.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(871*SCALE_FACTOR), int(351*SCALE_FACTOR)))
        self.search_cont.setTitle("")


        # search element contents
        if True:
            self.search_cont.setObjectName("search_cont")
            self.search_term_input = QtWidgets.QGroupBox(self.search_cont)
            self.search_term_input.setGeometry(QtCore.QRect(int(370*SCALE_FACTOR), int(110*SCALE_FACTOR), int(231*SCALE_FACTOR), int(71*SCALE_FACTOR)))
            self.search_term_input.setObjectName("search_term_input")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.search_term_input)
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.st_label = QtWidgets.QLabel(self.search_term_input)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.st_label.setFont(font)
            self.st_label.setAlignment(QtCore.Qt.AlignCenter)
            self.st_label.setObjectName("st_label")
            self.verticalLayout_2.addWidget(self.st_label)
            self.st_input = QtWidgets.QTextEdit(self.search_term_input)
            self.st_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.st_input.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
            self.st_input.setAcceptRichText(True)
            self.st_input.setObjectName("st_input")
            self.verticalLayout_2.addWidget(self.st_input)
            self.search_info = QtWidgets.QTextBrowser(self.search_cont)
            self.search_info.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(351*SCALE_FACTOR), int(331*SCALE_FACTOR)))
            self.search_info.setObjectName("search_info")
            self.file_term_input = QtWidgets.QGroupBox(self.search_cont)
            self.file_term_input.setGeometry(QtCore.QRect(int(370*SCALE_FACTOR), int(190*SCALE_FACTOR), int(231*SCALE_FACTOR), int(71*SCALE_FACTOR)))
            self.file_term_input.setObjectName("file_term_input")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.file_term_input)
            self.verticalLayout_3.setObjectName("verticalLayout_3")
            self.st_input.textChanged.connect(__search_switch)

        # file term elements
        if True:
            self.ft_label = QtWidgets.QLabel(self.file_term_input)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.ft_label.setFont(font)
            self.ft_label.setAlignment(QtCore.Qt.AlignCenter)
            self.ft_label.setObjectName("ft_label")
            self.verticalLayout_3.addWidget(self.ft_label)
            self.ft_input = QtWidgets.QComboBox(self.file_term_input)
            self.ft_input.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.file_term_dropdown(self.ft_input)
            self.ft_input.setObjectName("ft_input")
            self.verticalLayout_3.addWidget(self.ft_input)
            self.location_container = QtWidgets.QGroupBox(self.search_cont)
            self.location_container.setGeometry(QtCore.QRect(int(630*SCALE_FACTOR), int(210*SCALE_FACTOR), int(221*SCALE_FACTOR), int(71*SCALE_FACTOR)))
            self.location_container.setObjectName("location_container")
            self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.location_container)
            self.verticalLayout_23.setObjectName("verticalLayout_23")
            self.location_label = QtWidgets.QLabel(self.location_container)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.location_label.setFont(font)
            self.location_label.setAlignment(QtCore.Qt.AlignCenter)
            self.location_label.setObjectName("location_label")
            self.verticalLayout_23.addWidget(self.location_label)
            self.location_input = QtWidgets.QTextEdit(self.location_container)
            self.location_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.location_input.setObjectName("location_input")
            self.verticalLayout_23.addWidget(self.location_input)
            self.no_jobs_container = QtWidgets.QGroupBox(self.search_cont)
            self.no_jobs_container.setGeometry(QtCore.QRect(int(370*SCALE_FACTOR), int(270*SCALE_FACTOR), int(231*SCALE_FACTOR), int(71*SCALE_FACTOR)))
            self.no_jobs_container.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
            self.no_jobs_container.setObjectName("no_jobs_container")
            self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.no_jobs_container)
            self.verticalLayout_21.setObjectName("verticalLayout_21")
            self.location_input.textChanged.connect(__location_switch)

        # number of jobs to search
        if True:
            self.no_jobs_label = QtWidgets.QLabel(self.no_jobs_container)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.no_jobs_label.setFont(font)
            self.no_jobs_label.setAlignment(QtCore.Qt.AlignCenter)
            self.no_jobs_label.setObjectName("no_jobs_label")
            self.verticalLayout_21.addWidget(self.no_jobs_label)
            self.no_jobs_input = QtWidgets.QTextEdit(self.no_jobs_container)
            self.no_jobs_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.no_jobs_input.setObjectName("no_jobs_input")
            self.verticalLayout_21.addWidget(self.no_jobs_input)
            self.no_jobs_input.textChanged.connect(__find_amt_switch)

        # linkedin info fields
        if True:
            self.linkedin_info_groupBox = QtWidgets.QGroupBox(self.search_cont)
            self.linkedin_info_groupBox.setEnabled(False)
            self.linkedin_info_groupBox.setGeometry(QtCore.QRect(int(630*SCALE_FACTOR), int(10*SCALE_FACTOR), int(221*SCALE_FACTOR), int(191*SCALE_FACTOR)))
            self.linkedin_info_groupBox.setObjectName("linkedin_info_groupBox")
            self.lk_username = QtWidgets.QLabel(self.linkedin_info_groupBox)
            self.lk_username.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(20*SCALE_FACTOR), int(201*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lk_username.setFont(font)
            self.lk_username.setAlignment(QtCore.Qt.AlignCenter)
            self.lk_username.setObjectName("lk_username")
            self.lk_username_in = QtWidgets.QTextEdit(self.linkedin_info_groupBox)
            self.lk_username_in.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(50*SCALE_FACTOR), int(201*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            self.lk_username_in.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.lk_username_in.setObjectName("lk_username_in")
            self.lk_poassword = QtWidgets.QLabel(self.linkedin_info_groupBox)
            self.lk_poassword.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(80*SCALE_FACTOR), int(201*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lk_poassword.setFont(font)
            self.lk_poassword.setAlignment(QtCore.Qt.AlignCenter)
            self.lk_poassword.setObjectName("lk_poassword")
            self.lk_password_in = QtWidgets.QTextEdit(self.linkedin_info_groupBox)
            self.lk_password_in.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(120*SCALE_FACTOR), int(201*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            self.lk_password_in.setAcceptDrops(True)
            self.lk_password_in.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhMultiLine|QtCore.Qt.ImhSensitiveData)
            self.lk_password_in.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.lk_password_in.setObjectName("lk_password_in")
            self.lk_checkbox = QtWidgets.QCheckBox(self.linkedin_info_groupBox)
            self.lk_checkbox.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(140*SCALE_FACTOR), int(281*SCALE_FACTOR), int(31*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lk_checkbox.setFont(font)
            self.lk_checkbox.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.lk_checkbox.setChecked(False)
            self.lk_checkbox.setObjectName("lk_checkbox")
            self.job_board = QtWidgets.QGroupBox(self.search_cont)
            self.job_board.setGeometry(QtCore.QRect(int(370*SCALE_FACTOR), int(10*SCALE_FACTOR), int(231*SCALE_FACTOR), int(91*SCALE_FACTOR)))
            self.job_board.setObjectName("job_board")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.job_board)
            self.verticalLayout.setObjectName("verticalLayout")
            self.lk_password_in.textChanged.connect(__password_switch)
            self.lk_username_in.textChanged.connect(__username_switch)

        # job board label
        if True:
            self.jb_label = QtWidgets.QLabel(self.job_board)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.jb_label.setFont(font)
            self.jb_label.setAlignment(QtCore.Qt.AlignCenter)
            self.jb_label.setObjectName("jb_label")
            self.verticalLayout.addWidget(self.jb_label)

        # job board dropdown
        if True:
            self.jb_dropdown = QtWidgets.QComboBox(self.job_board)
            self.jb_dropdown.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.jb_dropdown.setObjectName("jb_dropdown")
            self.jb_dropdown.addItem("")
            self.jb_dropdown.addItem("")
            self.jb_dropdown.activated.connect(__linkedin_forms_toggle)
            self.verticalLayout.addWidget(self.jb_dropdown)

        # activate (search) button
        if True:
            self.search_button_container = QtWidgets.QGroupBox(self.search_cont)
            self.search_button_container.setEnabled(True)
            self.search_button_container.setGeometry(QtCore.QRect(int(630*SCALE_FACTOR), int(290*SCALE_FACTOR), int(221*SCALE_FACTOR), int(51*SCALE_FACTOR)))
            self.search_button_container.setObjectName("search_button_container")
            self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.search_button_container)
            self.verticalLayout_30.setObjectName("verticalLayout_30")
            self.search_button = QtWidgets.QPushButton(self.search_button_container)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(False)
            font.setWeight(50)
            self.search_button.setFont(font)
            self.search_button.setObjectName("search_button")
            self.search_button.setEnabled(False)
            self.verticalLayout_30.addWidget(self.search_button)

            self.search_button.clicked.connect(__run_search)

        # sets widgets to front
        self.search_button_container.raise_()
        self.job_board.raise_()
        self.search_term_input.raise_()
        self.search_info.raise_()
        self.file_term_input.raise_()
        self.location_container.raise_()
        self.no_jobs_container.raise_()
        self.linkedin_info_groupBox.raise_()
        self.MainTab.addTab(self.Search, "")

    def __setup_clf_tab(self):

        def __toggle_activate_button():
            if self.clf_term_input.currentText() !='None':
                self.activate_classifier_button.setEnabled(True)
                self.open_results_button.setEnabled(True)
            else:
                self.activate_classifier_button.setEnabled(False)
                self.open_results_button.setEnabled(False)

        # TODO - hook in classifier and check pertinent conditions
        def __run_classifier():
            self.__toggle_other_tabs(False,self.Classify)
            self.activate_classifier_button.setEnabled(False)
            self.open_results_button.setEnabled(False)
            file_term = self.clf_term_input.currentText()
            clfI = QWorkerCompatibleClassificationInterface(file_term,1,mode='live',no_labels=2)
            self.ThreadPool.start(clfI)
            clfI.signals.finished.connect(lambda: self.search_button.setEnabled(True))
            clfI.signals.finished.connect(lambda: self.__toggle_other_tabs(True))
            clfI.signals.finished.connect(lambda: self.open_results_button(True))

        def __show_results():
            if self.clf_term_input.currentText() !='None':
                self.open_results_button.setEnabled(True)
                resultwindow = QtWidgets.QMainWindow()
                result_ui = ResultsWindow(resultwindow,self.clf_term_input.currentText())
                resultwindow.show()
            else:
                self.clf_term_input.setEnabled(False)

        self.Classify = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Classify.sizePolicy().hasHeightForWidth())
        self.Classify.setSizePolicy(sizePolicy)
        self.Classify.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.Classify.setObjectName("Classify")

        # overall border elements
        self.clf_container = QtWidgets.QGroupBox(self.Classify)
        self.clf_container.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(871*SCALE_FACTOR), int(351*SCALE_FACTOR)))
        self.clf_container.setTitle("")
        self.clf_container.setObjectName("clf_container")

        # file/classification term elements
        if True:
            self.clf_term_container = QtWidgets.QGroupBox(self.clf_container)
            self.clf_term_container.setGeometry(QtCore.QRect(int(370*SCALE_FACTOR), int(10*SCALE_FACTOR), int(271*SCALE_FACTOR), int(91*SCALE_FACTOR)))
            self.clf_term_container.setObjectName("clf_term_container")
            self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.clf_term_container)
            self.verticalLayout_4.setObjectName("verticalLayout_4")
            self.clf_term_label = QtWidgets.QLabel(self.clf_term_container)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.clf_term_label.setFont(font)
            self.clf_term_label.setAlignment(QtCore.Qt.AlignCenter)
            self.clf_term_label.setObjectName("clf_term_label")
            self.verticalLayout_4.addWidget(self.clf_term_label)
            self.clf_term_input = QtWidgets.QComboBox(self.clf_term_container)
            self.clf_term_input.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.file_term_dropdown(self.clf_term_input)
            self.clf_term_input.setObjectName("clf_term_input")
            self.verticalLayout_4.addWidget(self.clf_term_input)

            self.clf_term_input.currentTextChanged.connect(__toggle_activate_button)

        # info text
        if True:
            self.clf_info = QtWidgets.QTextBrowser(self.clf_container)
            self.clf_info.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(351*SCALE_FACTOR), int(331*SCALE_FACTOR)))
            self.clf_info.setObjectName("clf_info")


        # model manual input
        if True:
            self.clf_use_container = QtWidgets.QGroupBox(self.clf_container)
            self.clf_use_container.setGeometry(QtCore.QRect(int(650*SCALE_FACTOR), int(10*SCALE_FACTOR), int(211*SCALE_FACTOR), int(171*SCALE_FACTOR)))
            self.clf_use_container.setObjectName("clf_use_container")
            self.clf_model_label = QtWidgets.QLabel(self.clf_use_container)
            self.clf_model_label.setGeometry(QtCore.QRect(int(40*SCALE_FACTOR), int(10*SCALE_FACTOR), int(135*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.clf_model_label.setFont(font)
            self.clf_model_label.setAlignment(QtCore.Qt.AlignCenter)
            self.clf_model_label.setObjectName("clf_model_label")
            self.clf_model_input = QtWidgets.QTextEdit(self.clf_use_container)
            self.clf_model_input.setEnabled(False)
            self.clf_model_input.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(110*SCALE_FACTOR), int(191*SCALE_FACTOR), int(41*SCALE_FACTOR)))
            self.clf_model_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.clf_model_input.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
            self.clf_model_input.setAcceptRichText(True)
            self.clf_model_input.setObjectName("clf_model_input")
            self.auto_checkbox = QtWidgets.QCheckBox(self.clf_use_container)
            self.auto_checkbox.setEnabled(True)
            self.auto_checkbox.setGeometry(QtCore.QRect(int(40*SCALE_FACTOR), int(50*SCALE_FACTOR), int(191*SCALE_FACTOR), int(31*SCALE_FACTOR)))
            self.auto_checkbox.setChecked(True)
            self.auto_checkbox.setObjectName("auto_checkbox")

        # run button elements
        if True:
            self.clf_run_container = QtWidgets.QGroupBox(self.clf_container)

            self.clf_run_container.setGeometry(QtCore.QRect(int(650*SCALE_FACTOR), int(200*SCALE_FACTOR), int(211*SCALE_FACTOR), int(61*SCALE_FACTOR)))
            self.clf_run_container.setTitle("")
            self.clf_run_container.setObjectName("clf_run_container")
            self.gridLayout = QtWidgets.QGridLayout(self.clf_run_container)
            self.gridLayout.setObjectName("gridLayout")
            self.activate_classifier_button = QtWidgets.QPushButton(self.clf_run_container)
            self.activate_classifier_button.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";\n"
                                                          "")
            self.activate_classifier_button.setObjectName("activate_classifier_button")
            self.gridLayout.addWidget(self.activate_classifier_button, 0, 0, 1, 1)
            self.activate_classifier_button.setEnabled(False)
            self.activate_classifier_button.clicked.connect(__run_classifier)
        # results elements
        if True:
            self.results_container = QtWidgets.QGroupBox(self.clf_container)
            self.results_container.setGeometry(QtCore.QRect(int(650*SCALE_FACTOR), int(280*SCALE_FACTOR), int(211*SCALE_FACTOR), int(61*SCALE_FACTOR)))
            self.results_container.setObjectName("results_container")
            self.verticalLayout_52 = QtWidgets.QVBoxLayout(self.results_container)
            self.verticalLayout_52.setObjectName("verticalLayout_52")
            self.open_results_button = QtWidgets.QPushButton(self.results_container)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.open_results_button.setFont(font)
            self.open_results_button.setObjectName("open_results_button")
            self.verticalLayout_52.addWidget(self.open_results_button)
            self.open_results_button.clicked.connect(__show_results)
            self.open_results_button.setEnabled(False)
        self.MainTab.addTab(self.Classify, "")

    def __setup_train_tab(self):


        def __get_train_data(database):
            job_data = {}
            with database:
                cur = database.cursor()
                job_data['total'] = cur.execute("SELECT COUNT(unique_id) from training").fetchall()

                for lab in ['Good Jobs','Bad Jobs','Neutral Jobs', "Ideal Jobs"]:
                    job_data[lab] = cur.execute("SELECT COUNT(unique_id) from training WHERE label = ?",(lab,)).fetchall()
            return job_data

        def __toggle_train_button():
            file_term = self.train_term_input.currentText()
            if file_term != 'None':
                iters = self.iter_input.toPlainText()
                try:
                    iters = int(iters)
                except TypeError:
                    # TODO add int requirment message
                    pass
                else:
                    if self.iter_use_default_check.isChecked() or iters:
                        # TODO add check for acceptable no of training data
                        if file_term in self.__get_file_terms():
                            job_data = __get_train_data(sqlite3.connect(os.path.join(os.getcwd(),
                                                                                     file_term,
                                                                                     f'{file_term}.db')))
                            self.train_button.setEnabled(True)
                            return
                        else:
                            self.train_button.setEnabled(False)




            # disables if any conditions fail
            self.train_button.setEnabled(False)

        def __sort_train_button():
            if self.train_term_input.currentText() != 'None':
                self.train_term_input.setEnabled(True)
                sortwindow = QtWidgets.QMainWindow()
                ui = TrainSelectWindow(sortwindow,self.train_term_input.currentText())
                sortwindow.show()
            else:
                self.train_term_input.setEnabled(False)


        def __run_training():
            self.train_button.setEnabled(False)
            self.__toggle_other_tabs(False,self.Train)
            file_term = self.train_term_input.currentText()
            iterations = int(self.iter_input.toPlainText())
            handler = QWorkerCompatibleClassificationInterface(file_term=file_term,
                                                               iterations=iterations,
                                                               no_labels=2,
                                                               mode='train')

            def test(val):
                print(val)
            handler.signals.progress.connect(lambda val : self.train_progress.setValue(val))
            handler.signals.progress.connect(test)
            handler.signals.finished.connect(lambda : self.__toggle_other_tabs(True))
            handler.signals.finished.connect(lambda : self.train_button.setEnabled(True))
            self.ThreadPool.start(handler)

            # TODO hook up with training module + add condition for insufficient training data

        self.Train = QtWidgets.QWidget()
        self.Train.setObjectName("Train")
        self.train_container = QtWidgets.QGroupBox(self.Train)
        self.train_container.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(871*SCALE_FACTOR), int(351*SCALE_FACTOR)))
        self.train_container.setTitle("")
        self.train_container.setObjectName("train_container")

        # train / file term elements and sort button elements
        if True:
            self.train_term_container = QtWidgets.QGroupBox(self.train_container)
            self.train_term_container.setGeometry(QtCore.QRect(int(360*SCALE_FACTOR), int(10*SCALE_FACTOR), int(221*SCALE_FACTOR), int(141*SCALE_FACTOR)))
            self.train_term_container.setObjectName("train_term_container")
            self.train_term_label = QtWidgets.QLabel(self.train_term_container)
            self.train_term_label.setGeometry(QtCore.QRect(int(30*SCALE_FACTOR), int(10*SCALE_FACTOR), int(155*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.train_term_label.setFont(font)
            self.train_term_label.setAlignment(QtCore.Qt.AlignCenter)
            self.train_term_label.setObjectName("train_term_label")
            self.train_term_input = QtWidgets.QComboBox(self.train_term_container)
            self.train_term_input.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(39*SCALE_FACTOR), int(201*SCALE_FACTOR), int(31*SCALE_FACTOR)))
            self.train_term_input.setLayoutDirection(QtCore.Qt.LeftToRight)

            self.train_term_input.setObjectName("train_term_input")
            self.file_term_dropdown(self.train_term_input)
            # open sorting button
            self.manual_sort_button = QtWidgets.QPushButton(self.train_term_container)
            self.manual_sort_button.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(82*SCALE_FACTOR), int(201*SCALE_FACTOR), int(51*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(15)
            self.manual_sort_button.setFont(font)
            self.manual_sort_button.setObjectName("manual_sort_button")
            self.train_term_input.activated.connect(__toggle_train_button)
            self.manual_sort_button.clicked.connect(__sort_train_button)
            self.manual_sort_button.setEnabled(False)

        #progress bar
        if True:
            self.train_progress = QtWidgets.QProgressBar(self.train_container)
            self.train_progress.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(320*SCALE_FACTOR), int(851*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            self.train_progress.setMaximum(100)
            self.train_progress.setProperty("value", 0)
            self.train_progress.setOrientation(QtCore.Qt.Horizontal)
            self.train_progress.setObjectName("train_progress")

        # iteration form elements
        if True:
            self.iter_per_round = QtWidgets.QGroupBox(self.train_container)
            self.iter_per_round.setGeometry(QtCore.QRect(int(590*SCALE_FACTOR), int(10*SCALE_FACTOR), int(271*SCALE_FACTOR), int(141*SCALE_FACTOR)))
            self.iter_per_round.setObjectName("iter_per_round")
            self.iter_per_round_label = QtWidgets.QLabel(self.iter_per_round)
            self.iter_per_round_label.setGeometry(QtCore.QRect(int(40*SCALE_FACTOR), int(10*SCALE_FACTOR), int(211*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.iter_per_round_label.setFont(font)
            self.iter_per_round_label.setAlignment(QtCore.Qt.AlignCenter)
            self.iter_per_round_label.setObjectName("iter_per_round_label")
            self.iter_input = QtWidgets.QTextEdit(self.iter_per_round)
            self.iter_input.setEnabled(False)
            self.iter_input.setGeometry(QtCore.QRect(int(40*SCALE_FACTOR), int(80*SCALE_FACTOR), int(191*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setFamily("MingLiU_HKSCS-ExtB")
            font.setStrikeOut(False)
            self.iter_input.setFont(font)
            self.iter_input.setInputMethodHints(QtCore.Qt.ImhDigitsOnly | QtCore.Qt.ImhMultiLine)
            self.iter_input.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.iter_input.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
            self.iter_input.setAcceptRichText(True)
            self.iter_input.setObjectName("iter_input")
            self.iter_use_default_check = QtWidgets.QCheckBox(self.iter_per_round)
            self.iter_use_default_check.setEnabled(True)
            self.iter_use_default_check.setGeometry(QtCore.QRect(int(40*SCALE_FACTOR), int(40*SCALE_FACTOR), int(211*SCALE_FACTOR), int(31*SCALE_FACTOR)))
            self.iter_use_default_check.setCheckable(True)
            self.iter_use_default_check.setChecked(True)
            self.iter_use_default_check.setObjectName("iter_use_default_check")
            self.iter_input.textChanged.connect(__toggle_train_button)
        # Train button and advanced option buttons elements
        if True:
            self.train_info = QtWidgets.QTextBrowser(self.train_container)
            self.train_info.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(341*SCALE_FACTOR), int(301*SCALE_FACTOR)))
            self.train_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.train_info.setObjectName("train_info")
            self.train_confandrun_buttons_container = QtWidgets.QGroupBox(self.train_container)
            self.train_confandrun_buttons_container.setGeometry(QtCore.QRect(int(360*SCALE_FACTOR), int(160*SCALE_FACTOR), int(501*SCALE_FACTOR), int(71*SCALE_FACTOR)))
            self.train_confandrun_buttons_container.setObjectName("frame")
            self.select_processing_options_button = QtWidgets.QPushButton(self.train_confandrun_buttons_container)
            self.select_processing_options_button.setGeometry(QtCore.QRect(int(230*SCALE_FACTOR), int(40*SCALE_FACTOR), int(261*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            self.select_processing_options_button.setObjectName("select_processing_options_button")
            self.train_button = QtWidgets.QPushButton(self.train_confandrun_buttons_container)
            self.train_button.setEnabled(False)
            self.train_button.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(211*SCALE_FACTOR), int(51*SCALE_FACTOR)))
            self.train_button.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";\n"
                                            "")
            self.train_button.setObjectName("train_button")
            self.select_models_button = QtWidgets.QPushButton(self.train_confandrun_buttons_container)
            self.select_models_button.setGeometry(QtCore.QRect(int(230*SCALE_FACTOR), int(10*SCALE_FACTOR), int(261*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            self.select_models_button.setObjectName("select_models_button")
            self.train_button.clicked.connect(__run_training)
        self.MainTab.addTab(self.Train, "")

    def __setup_combined_tab(self):

        # container used to check if all required forms are filled
        # 1 - search term
        # 2 - No. of Jobs to Find
        # 3 - Location
        # 4 - Username, only required for linkedin
        # 5 - Password - only required for linkedin
        # 6 - File term - must be set when running combined search to get models
        run_flag_container = {1: False, 2: False, 3: False, 4: True, 5: True, 6: False}

        def __search_switch():
            if self.st_input_2.toPlainText():
                run_flag_container[1] = True
            else:
                run_flag_container[1] = False
            __enable_run()
        def __file_term_switch():
            if self.ft_dropdown_input_2.currentText() != 'None':
                run_flag_container[6] = True
                self.open_results_button_2.setEnabled(True)

            else:
                run_flag_container[6] = False
                self.open_results_button_2.setEnabled(False)
            __enable_run()
        def __find_amt_switch():
            amt = self.no_jobs_input_2.toPlainText()
            try:
                amt = int(amt)
            except ValueError as e:
                print('input a number')
                run_flag_container[2] = False
            else:
                if amt:
                    run_flag_container[2] = True

                else:
                    run_flag_container[2] = False
            __enable_run()

        def __location_switch():
            if self.location_input_2.toPlainText():
                run_flag_container[3] = True
            else:
                run_flag_container[3] = False
            __enable_run()

        def __username_switch():
            if self.lk_username_in_2.toPlainText():
                run_flag_container[4] = True
            else:
                run_flag_container[4] = False
            __enable_run()

        def __password_switch():
            if self.lk_password_in_2.toPlainText():
                run_flag_container[5] = True
            else:
                run_flag_container[5] = False
            __enable_run()

        def __enable_run():
            if all([_ for _ in run_flag_container.values()]):
                self.run_button.setDisabled(False)
            else:
                self.run_button.setDisabled(True)

        # TODO hook in classify elements
        def __run_combined():

            def reactivate():
                self.run_button.setEnabled(True)
                self.ft_dropdown_input_2.setEnabled(True)
                self.__toggle_other_tabs(True)
                self.open_results_button_2.setEnabled(True)

            """ run a job search followed by classification"""

            self.run_button.setEnabled(False)
            self.ft_dropdown_input_2.setEnabled(False)
            self.__toggle_other_tabs(False,self.SearchClassify)
            self.open_results_button_2.setEnabled(False)

            search_term = self.st_input_2.toPlainText()
            file_term = self.ft_dropdown_input_2.currentText()
            location = self.location_input_2.toPlainText()
            jobs_to_find = int(self.no_jobs_input_2.toPlainText())

            if self.jb_dropdown_2.currentText() == 'LinkedIn':
                username = self.lk_username_in_2.toPlainText()
                if self.lk_checkbox_2.isChecked():
                    pass
                    # TODO setup secure saving of linkedin info
                client= LinkdinClient(search_term=search_term,
                                      file_term=file_term,
                                      location=location,
                                      jobs_to_find=jobs_to_find)
                worker = WorkerGeneric(client, [username, self.lk_password_in.toPlainText()])
                self.ThreadPool.start(worker)

            elif self.jb_dropdown_2.currentText() == 'Indeed':
                client = IndeedClient(search_term=search_term,
                                      file_term=file_term,
                                      location=location,
                                      jobs_to_find=jobs_to_find)
                worker = WorkerGeneric(client)
                self.ThreadPool.start(worker)

            clfI = QWorkerCompatibleClassificationInterface(file_term,1,mode='live',no_labels=2)
            worker.signals.finished.connect(lambda  : clfI.classify_live_jobs())
            clfI.signals.finished.connect (lambda  : reactivate())


        def __clinkedin_forms_toggle():
            if self.jb_dropdown_2.currentText() == 'LinkedIn':
                self.linkedin_info_groupBox_2.setDisabled(False)
                run_flag_container[4] = False
                run_flag_container[5] = False

            else:
                self.linkedin_info_groupBox_2.setDisabled(True)
                run_flag_container[4] = True
                run_flag_container[5] = True
            __enable_run()

        # TODO - link with results dipslay
        def __show_results():
            resultwindow = QtWidgets.QMainWindow()
            result_ui = ResultsWindow(resultwindow, self.ft_dropdown_input_2.currentText())
            resultwindow.show()

        self.SearchClassify = QtWidgets.QWidget()
        self.SearchClassify.setObjectName("SearchClassify")
        self.sc_field_container = QtWidgets.QGroupBox(self.SearchClassify)
        self.sc_field_container.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(871*SCALE_FACTOR), int(351*SCALE_FACTOR)))
        self.sc_field_container.setObjectName("sc_field_container")

        # job board elements
        if True:
            self.job_board_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.job_board_2.setGeometry(QtCore.QRect(int(440*SCALE_FACTOR), int(100*SCALE_FACTOR), int(211*SCALE_FACTOR), int(81*SCALE_FACTOR)))
            self.job_board_2.setObjectName("job_board_4")
            self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.job_board_2)
            self.verticalLayout_16.setObjectName("verticalLayout_16")
            self.jb_label_2 = QtWidgets.QLabel(self.job_board_2)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.jb_label_2.setFont(font)
            self.jb_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.jb_label_2.setObjectName("jb_label_2")
            self.verticalLayout_16.addWidget(self.jb_label_2)
            self.jb_dropdown_2 = QtWidgets.QComboBox(self.job_board_2)
            self.jb_dropdown_2.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.jb_dropdown_2.setObjectName("jb_dropdown_2")
            self.jb_dropdown_2.addItem("")
            self.jb_dropdown_2.addItem("")
            self.verticalLayout_16.addWidget(self.jb_dropdown_2)
            self.classifier_label_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.classifier_label_2.setGeometry(QtCore.QRect(int(660*SCALE_FACTOR), int(10*SCALE_FACTOR), int(201*SCALE_FACTOR), int(171*SCALE_FACTOR)))
            self.classifier_label_2.setObjectName("classifier_label_2")
            self.jb_dropdown_2.activated.connect(__clinkedin_forms_toggle)

        # manual model input elements
        if True:
            self.clf_model_label_2 = QtWidgets.QLabel(self.classifier_label_2)
            self.clf_model_label_2.setGeometry(QtCore.QRect(int(40*SCALE_FACTOR), int(10*SCALE_FACTOR), int(135*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.clf_model_label_2.setFont(font)
            self.clf_model_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.clf_model_label_2.setObjectName("clf_model_label_2")
            self.clf_model_input_2 = QtWidgets.QTextEdit(self.classifier_label_2)
            self.clf_model_input_2.setEnabled(False)
            self.clf_model_input_2.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(100*SCALE_FACTOR), int(181*SCALE_FACTOR), int(41*SCALE_FACTOR)))
            self.clf_model_input_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.clf_model_input_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
            self.clf_model_input_2.setAcceptRichText(True)
            self.clf_model_input_2.setObjectName("clf_model_input_2")
            self.clf_auto_checkbox2 = QtWidgets.QCheckBox(self.classifier_label_2)
            self.clf_auto_checkbox2.setEnabled(True)
            self.clf_auto_checkbox2.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(50*SCALE_FACTOR), int(191*SCALE_FACTOR), int(31*SCALE_FACTOR)))
            self.clf_auto_checkbox2.setChecked(True)
            self.clf_auto_checkbox2.setObjectName("clf_auto_checkbox2")


        #linkden info elements
        if True:
            self.linkedin_info_groupBox_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.linkedin_info_groupBox_2.setEnabled(False)
            self.linkedin_info_groupBox_2.setGeometry(QtCore.QRect(int(240*SCALE_FACTOR), int(190*SCALE_FACTOR), int(411*SCALE_FACTOR), int(151*SCALE_FACTOR)))
            self.linkedin_info_groupBox_2.setObjectName("linkedin_info_groupBox_2")
            self.lk_password_in_2 = QtWidgets.QTextEdit(self.linkedin_info_groupBox_2)
            self.lk_password_in_2.setGeometry(QtCore.QRect(int(111*SCALE_FACTOR), int(30*SCALE_FACTOR), int(161*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            self.lk_password_in_2.setAcceptDrops(True)
            self.lk_password_in_2.setInputMethodHints(
                QtCore.Qt.ImhHiddenText | QtCore.Qt.ImhMultiLine | QtCore.Qt.ImhSensitiveData)
            self.lk_password_in_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.lk_password_in_2.setObjectName("lk_password_in_2")
            self.lk_checkbox_2 = QtWidgets.QCheckBox(self.linkedin_info_groupBox_2)
            self.lk_checkbox_2.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(110*SCALE_FACTOR), int(261*SCALE_FACTOR), int(27*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lk_checkbox_2.setFont(font)
            self.lk_checkbox_2.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.lk_checkbox_2.setChecked(False)
            self.lk_checkbox_2.setObjectName("lk_checkbox_2")
            self.lk_username_in_2 = QtWidgets.QTextEdit(self.linkedin_info_groupBox_2)
            self.lk_username_in_2.setGeometry(QtCore.QRect(int(110*SCALE_FACTOR), int(80*SCALE_FACTOR), int(161*SCALE_FACTOR), int(21*SCALE_FACTOR)))
            self.lk_username_in_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.lk_username_in_2.setObjectName("lk_username_in_2")
            self.lk_password_label_2 = QtWidgets.QLabel(self.linkedin_info_groupBox_2)
            self.lk_password_label_2.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(60*SCALE_FACTOR), int(91*SCALE_FACTOR), int(51*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lk_password_label_2.setFont(font)
            self.lk_password_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.lk_password_label_2.setObjectName("lk_paassword_label_2")
            self.lk_username_label_2 = QtWidgets.QLabel(self.linkedin_info_groupBox_2)
            self.lk_username_label_2.setGeometry(QtCore.QRect(int(14*SCALE_FACTOR), int(10*SCALE_FACTOR), int(91*SCALE_FACTOR), int(51*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.lk_username_label_2.setFont(font)
            self.lk_username_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.lk_username_label_2.setObjectName("lk_username_label_2")
            self.location_container_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.location_container_2.setGeometry(QtCore.QRect(int(440*SCALE_FACTOR), int(10*SCALE_FACTOR), int(211*SCALE_FACTOR), int(81*SCALE_FACTOR)))
            self.location_container_2.setObjectName("location_container_2")
            self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.location_container_2)
            self.verticalLayout_24.setObjectName("verticalLayout_24")

            self.lk_password_in_2.textChanged.connect(__password_switch)
            self.lk_username_in_2.textChanged.connect(__username_switch)
        # location elements
        if True:
            self.location_label_2 = QtWidgets.QLabel(self.location_container_2)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.location_label_2.setFont(font)
            self.location_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.location_label_2.setObjectName("location_label_2")
            self.verticalLayout_24.addWidget(self.location_label_2)
            self.location_input_2 = QtWidgets.QTextEdit(self.location_container_2)
            self.location_input_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.location_input_2.setObjectName("location_input_2")
            self.verticalLayout_24.addWidget(self.location_input_2)
            self.location_input_2.textChanged.connect(__location_switch)
        # description elements'
        if True:
            self.sandc_info = QtWidgets.QTextBrowser(self.sc_field_container)
            self.sandc_info.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(10*SCALE_FACTOR), int(221*SCALE_FACTOR), int(211*SCALE_FACTOR)))
            self.sandc_info.setObjectName("sandc_info")

        # activate button elements
        if True:
            self.run_cont_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.run_cont_2.setGeometry(QtCore.QRect(int(660*SCALE_FACTOR), int(190*SCALE_FACTOR), int(201*SCALE_FACTOR), int(81*SCALE_FACTOR)))
            self.run_cont_2.setObjectName("run_cont_2")
            self.verticalLayout_43 = QtWidgets.QVBoxLayout(self.run_cont_2)
            self.verticalLayout_43.setObjectName("verticalLayout_43")
            self.run_button = QtWidgets.QPushButton(self.run_cont_2)
            self.run_button.setEnabled(False)
            font = QtGui.QFont()
            font.setPointSize(16)
            self.run_button.setFont(font)
            self.run_button.setObjectName("run_button")
            self.verticalLayout_43.addWidget(self.run_button)
            self.run_button.clicked.connect(__run_combined)
        # file term elements
        if True:
            self.file_term_container_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.file_term_container_2.setGeometry(QtCore.QRect(int(10*SCALE_FACTOR), int(240*SCALE_FACTOR), int(221*SCALE_FACTOR), int(101*SCALE_FACTOR)))
            self.file_term_container_2.setObjectName("file_term_container_2")
            self.ft_label_2 = QtWidgets.QLabel(self.file_term_container_2)
            self.ft_label_2.setGeometry(QtCore.QRect(int(60*SCALE_FACTOR), int(10*SCALE_FACTOR), int(78*SCALE_FACTOR), int(23*SCALE_FACTOR)))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.ft_label_2.setFont(font)
            self.ft_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.ft_label_2.setObjectName("ft_label_2")

            self.ft_dropdown_input_2 = QtWidgets.QComboBox(self.file_term_container_2)
            self.ft_dropdown_input_2.setLayoutDirection(QtCore.Qt.LeftToRight)
            self.ft_dropdown_input_2.setGeometry(
                QtCore.QRect(int(10 * SCALE_FACTOR), int(49 * SCALE_FACTOR), int(191 * SCALE_FACTOR), int(31 * SCALE_FACTOR)))
            #self.ft_dropdown_input_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.file_term_dropdown(self.ft_dropdown_input_2)
            self.ft_dropdown_input_2.setObjectName("ft_dropdown_input_2")
            self.ft_dropdown_input_2.activated.connect(__file_term_switch)
        # search term elements
        if True:
            self.st_container_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.st_container_2.setGeometry(QtCore.QRect(int(240*SCALE_FACTOR), int(10*SCALE_FACTOR), int(191*SCALE_FACTOR), int(81*SCALE_FACTOR)))
            self.st_container_2.setObjectName("st_container_2")
            self.verticalLayout_45 = QtWidgets.QVBoxLayout(self.st_container_2)
            self.verticalLayout_45.setObjectName("verticalLayout_45")
            self.st_label_2 = QtWidgets.QLabel(self.st_container_2)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.st_label_2.setFont(font)
            self.st_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.st_label_2.setObjectName("st_label_2")
            self.verticalLayout_45.addWidget(self.st_label_2)
            self.st_input_2 = QtWidgets.QTextEdit(self.st_container_2)
            self.st_input_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.st_input_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
            self.st_input_2.setAcceptRichText(True)
            self.st_input_2.setObjectName("st_input_2")
            self.verticalLayout_45.addWidget(self.st_input_2)
            self.st_input_2.textChanged.connect(__search_switch)
        # open results folder elements
        if True:
            self.results_container_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.results_container_2.setGeometry(QtCore.QRect(int(660*SCALE_FACTOR), int(280*SCALE_FACTOR), int(201*SCALE_FACTOR), int(61*SCALE_FACTOR)))
            self.results_container_2.setObjectName("results_container_2")
            self.verticalLayout_51 = QtWidgets.QVBoxLayout(self.results_container_2)
            self.verticalLayout_51.setObjectName("verticalLayout_51")
            self.open_results_button_2 = QtWidgets.QPushButton(self.results_container_2)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.open_results_button_2.setFont(font)
            self.open_results_button_2.setObjectName("open_results_button_2")

            self.open_results_button_2.clicked.connect(__show_results)
            self.open_results_button_2.setEnabled(False)
        # job search no elements
        if True:
            self.verticalLayout_51.addWidget(self.open_results_button_2)
            self.no_jobs_container_2 = QtWidgets.QGroupBox(self.sc_field_container)
            self.no_jobs_container_2.setGeometry(QtCore.QRect(int(240*SCALE_FACTOR), int(100*SCALE_FACTOR), int(191*SCALE_FACTOR), int(81*SCALE_FACTOR)))
            self.no_jobs_container_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
            self.no_jobs_container_2.setObjectName("no_jobs_container_2")



            self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.no_jobs_container_2)
            self.verticalLayout_22.setObjectName("verticalLayout_22")
            self.no_jobs_label_2 = QtWidgets.QLabel(self.no_jobs_container_2)
            font = QtGui.QFont()
            font.setPointSize(14)
            self.no_jobs_label_2.setFont(font)
            self.no_jobs_label_2.setAlignment(QtCore.Qt.AlignCenter)
            self.no_jobs_label_2.setObjectName("no_jobs_label_2")
            self.verticalLayout_22.addWidget(self.no_jobs_label_2)
            self.no_jobs_input_2 = QtWidgets.QTextEdit(self.no_jobs_container_2)
            self.no_jobs_input_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.no_jobs_input_2.setObjectName("no_jobs_input_2")
            self.verticalLayout_22.addWidget(self.no_jobs_input_2)

            self.no_jobs_input_2.textChanged.connect(__find_amt_switch)
        self.MainTab.addTab(self.SearchClassify, "")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(SCALE_FACTOR*894), int(SCALE_FACTOR*464))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainTab = QtWidgets.QTabWidget(self.centralwidget)
        self.MainTab.setGeometry(QtCore.QRect(int(0*SCALE_FACTOR), int(40*SCALE_FACTOR), int(900*SCALE_FACTOR), int(405*SCALE_FACTOR)))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainTab.sizePolicy().hasHeightForWidth())
        self.MainTab.setSizePolicy(sizePolicy)
        self.MainTab.setAutoFillBackground(True)
        self.MainTab.setObjectName("MainTab")
        self.__setup_info_tab()
        self.__setup_search_tab()
        self.__setup_train_tab()
        self.__setup_clf_tab()
        self.__setup_combined_tab()
        self.__setup_top_menu()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(int(0*SCALE_FACTOR), int(0*SCALE_FACTOR), int(894*SCALE_FACTOR), int(21*SCALE_FACTOR)))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.MainTab.setCurrentIndex(1)
        self.iter_use_default_check.toggled['bool'].connect(self.iter_input.setDisabled)
        self.clf_auto_checkbox2.toggled['bool'].connect(self.clf_model_input_2.setDisabled)
        self.auto_checkbox.toggled['bool'].connect(self.clf_model_input.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.intro_info.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Welcome to SmartJobClassifier, a scikit-learn based application used to automatically download and sort through online job board postings. If this is your first time using this application you will need to download either chromedriver (if you use Chrome) or geckodriver (if you use Firefox) using the corresponding buttons in the top panel. These can also be used to download the latest version when a newer one is released. Once this is done, you should start on the \'Search\' tab, and from there go to \'Train\' and then \'Classify\'. Detailed instructions are given on each tab, as well as within the readme. </span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">If you\'re willing to do so, please send over usage information using the \'Sent Usage Info\' button in the top panel, all this does is sent me a notification that a new user is using this application, and lets me get an idea of how many people are using this. If you run into a bug, you can use \'Report an Issue\' to send me a brief description of what you were doing and what the issue is.</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">If you would like to contribute, you can either visit the repository at https://github.com/TheMagicalPlace/JobPostingClassifier for more information. While all feedback is appreciated, I especially could use your any training data, since having a wider variety of results will allow me to keep improving this application.</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">If you like my work be sure to give me a software development job and/or visit my repo at www.olivegarden.com. </span></p></body></html>"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Info), _translate("MainWindow", "Info"))
        self.st_label.setText(_translate("MainWindow", "Search Term"))
        self.st_input.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.search_info.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Here you can search and download job postings from any of the available job boards. If using LinkedIn a username and password is currently required, and the option to save your credentials for future use is available. Below information is given about what should be input into each field. Note that all terms besides login credentials are not case sensative.</span></p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">FIELDS</span></p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Job Board:</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Selecting which job board to get data from. Note that with linkedin it is required that you log in. Can optionally save LinkedIn login credentials if desired.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Location:</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">The location for which to search for job postings.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Search Term:</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">The term to search the selected job boards.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Equivalent File Term:</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Used to specify which job data folder to save the results of the search to. This defaults to the search term, however in cases where a given field of related jobs can have multiple titles or search terms it is often desirable to include them all as a part of the same dataset for model training and sorting.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">For example, if \'Computer Programmer\' was previously searched, searching &quot;Entry Level Computer Programmer&quot; and setting the equivalent file term to \'Computer Programmer\' would put the results from &quot;Entry Level Computer Programmer&quot; in the same location as those from searching \'Computer Programmer\'.</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">No. of Jobs to Find:</span></p>\n"
                                            "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Number of NEW job postings to find, postings that have already been found and downloaded don\'t count when determining when to stop.</span></p></body></html>"))
        self.ft_label.setText(_translate("MainWindow", "Equivalent File Term"))
        self.location_label.setText(_translate("MainWindow", "Location"))
        self.no_jobs_label.setText(_translate("MainWindow", "No. of Jobs to Find"))
        self.lk_username.setText(_translate("MainWindow", "Username"))
        self.lk_poassword.setText(_translate("MainWindow", "Password"))
        self.lk_checkbox.setText(_translate("MainWindow", "Save Login Info"))
        self.jb_label.setText(_translate("MainWindow", "Job Board"))
        self.jb_dropdown.setItemText(0, _translate("MainWindow", "Indeed"))
        self.jb_dropdown.setItemText(1, _translate("MainWindow", "LinkedIn"))
        self.search_button.setText(_translate("MainWindow", "Search"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Search), _translate("MainWindow", "Search"))
        self.clf_term_label.setText(_translate("MainWindow", "Classification Term"))
        #self.clf_term_input.setHtml(_translate("MainWindow",
        #                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        #                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        #                                       "p, li { white-space: pre-wrap; }\n"
        #                                       "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        #                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.clf_info.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Used to classify job postings that have already been downloaded but not yet classified. Note that before using this feature you must have previously trained models for the search/file term you are trying to classify. Further information on this is given unter the \'Train\' tab as well as in the readme. Note that the classification term is not case sensative.</span></p>\n"
                                         "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">FIELDS</span></p>\n"
                                         "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Classification/File Term:</span></p>\n"
                                         "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Used to tell the classifier which  search/file term the classification model should be loaded from, as well as where to save the results to.</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Clasifier to Use:</span></p>\n"
                                         "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">It is highly reccomended that you leave this set to auto, however if you know what you\'re doing a model can be manually selected to run instead of the found best one.  </span></p></body></html>"))
        self.clf_model_label.setText(_translate("MainWindow", "Classifier To Use"))
        self.clf_model_input.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">input model name here</span></p>\n"
                                                "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p></body></html>"))
        self.auto_checkbox.setText(_translate("MainWindow", "Auto-Select Best Model"))
        self.activate_classifier_button.setText(_translate("MainWindow", "Activate"))
        self.open_results_button.setText(_translate("MainWindow", "Open Results Folder"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Classify), _translate("MainWindow", "Classify"))
        self.train_term_label.setText(_translate("MainWindow", "File Term"))
        #self.train_term_input.setHtml(_translate("MainWindow",
        #                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        #                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        #                                         "p, li { white-space: pre-wrap; }\n"
        #                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        #                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.manual_sort_button.setText(_translate("MainWindow", "Manually Sort Jobs"))
        self.train_progress.setFormat(_translate("MainWindow", "%p%"))
        self.iter_per_round_label.setText(_translate("MainWindow", "Iterations Per Round"))
        self.iter_input.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MingLiU_HKSCS-ExtB\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-style:italic;\">150</span></p></body></html>"))
        self.iter_use_default_check.setText(_translate("MainWindow", "Use Default (reccomended)"))
        self.train_info.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">This section is used to train classification models for use in job sorting. Can be used to create and train models from new data, or to update old models based on newly added data.</span></p>\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">INSTRUCTIONS</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">In order to create the models used in this program it is required that some initial information is supplied. This is done by downloading (via the \'Search Tab\') and manually sorting job postings according to whether the job posting is an \'Ideal\', \'Good\', \'Neutral\', or \'Bad\' job for you. It is reccomended that supply at least 100 jobs for the training data as well as ensuring that the way you are sorting them as accuratly as possible, however the more data you supply for training the more accurate the results will be, as well as reducing the impact of badly sorted jobs on the result. Once this is done you can run the training via \'Train Models\', the amount of time taken depends on the number of iterations and amount of training data, however 1-3 hours should be a typical amount of time for the training to complete.</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">So, in order the steps are:</span></p>\n"
                                           "<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-size:10pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Download job postings using the \'Search\' tab for the file term you are using.</li>\n"
                                           "<li style=\" font-size:10pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Sort the jobs using the \'Manually Sort Jobs\' Button.</li>\n"
                                           "<li style=\" font-size:10pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Run the training program via \'Train Models\'.</li></ol>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">FIELDS</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">File Term:</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">This should be the same term as the search term used previously if this is for completely new models, otherwise use the file term for which you want to update models for.</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Iterations Per Round:</span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:8px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">The number of times to train the models on the data, higher numbers will increase model accuracy, but take longer. Between 75-200 is reccomended, with minimal improvment for any higher amount. </span></p>\n"
                                           "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\"> </span></p></body></html>"))
        self.select_processing_options_button.setText(
            _translate("MainWindow", "Modify Data Preprocessing (Advanced)"))
        self.train_button.setText(_translate("MainWindow", "Train Models"))
        self.select_models_button.setText(_translate("MainWindow", "Select Models to Train (Advanced)"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.Train), _translate("MainWindow", "Train"))
        self.jb_label_2.setText(_translate("MainWindow", "Job Board"))
        self.jb_dropdown_2.setItemText(0, _translate("MainWindow", "Indeed"))
        self.jb_dropdown_2.setItemText(1, _translate("MainWindow", "LinkedIn"))
        self.clf_model_label_2.setText(_translate("MainWindow", "Classifier To Use"))
        self.clf_model_input_2.setHtml(_translate("MainWindow",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Entry Level Chemical Engineer</p>\n"
                                                  "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.clf_auto_checkbox2.setText(_translate("MainWindow", "Auto-Select Best Model"))
        self.lk_checkbox_2.setText(_translate("MainWindow", "Save Login Info"))
        self.lk_password_label_2.setText(_translate("MainWindow", "Password"))
        self.lk_username_label_2.setText(_translate("MainWindow", "Username"))
        self.location_label_2.setText(_translate("MainWindow", "Location"))
        self.sandc_info.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Please refer to the the Search and Classify tabs for information on each input field.</span></p></body></html>"))
        self.run_button.setText(_translate("MainWindow", "Run"))
        self.ft_label_2.setText(_translate("MainWindow", "File Term"))
        self.st_label_2.setText(_translate("MainWindow", "Search Term"))
        self.st_input_2.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.open_results_button_2.setText(_translate("MainWindow", "Show Results"))
        self.no_jobs_label_2.setText(_translate("MainWindow", "No. of Jobs to Find"))
        self.no_jobs_input_2.setHtml(_translate("MainWindow",
                                                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">100</p></body></html>"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.SearchClassify),
                                _translate("MainWindow", "Search + Classify"))
        self.report_issue_button.setText(_translate("MainWindow", "Report an Issue"))
        self.usage_button.setText(_translate("MainWindow", "Send Usage Info"))
        self.dl_1_button.setText(_translate("MainWindow", "Download Chromedriver"))
        self.dl_2_button.setText(_translate("MainWindow", "Download Geckodriver"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))

if __name__ == "__main__":
    import sys

    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = SJCGuiMain()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



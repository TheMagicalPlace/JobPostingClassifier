import os
import sqlite3
import webbrowser

from PyQt5 import QtCore, QtGui, QtWidgets

from ui import SCALE_FACTOR

class ResultsWindow(object):

    def __init__(self,window_obj,file_term):
        self.MainWindow = window_obj
        self.file_term = file_term
        self.database = sqlite3.connect(os.path.join(os.getcwd(),file_term,f'{file_term}.db'))
        self.current_uid = None
        self.current_job = None
        self.current_text = None
        self.link = None
        self.company = None
        self.location = None

        self.setupUi()
        with self.database:
            cur = self.database.cursor()
            self.results_jobs = cur.execute("""
                SELECT results.unique_id,results.description,results.job_title,metadata.link,metadata.company,metadata.location 
                FROM results 
                INNER JOIN metadata 
                ON results.unique_id = metadata.unique_id 
                WHERE results.label = 'Good Jobs' 
                OR results.label = 'Ideal Jobs'""").fetchall()
            self.results_jobs.append(None)

        if self.results_jobs[0] is not None:
            self.__get_next_result()
        else:
            self.__no_results_jobs_handler()

    def __get_next_result(self):
        nextuns = self.results_jobs.pop()
        if nextuns is not None:
            self.unique_id, self.current_text, self.current_job,self.link,self.company,self.location = nextuns
            self.job_desc_text.setText(self.current_text)
            self.jobtitle_info.setText(self.current_job)
            self.company_info.setText(self.company)
            self.location_info.setText(self.location)
        else:
            self.MainWindow.close()

    def __button_click_response_handler(self,button):

        response = button.text()+" Jobs"
        with self.database:
            cur = self.database.execute("INSERT INTO training VALUES(?,?,?,?)",
                                        (self.unique_id,response,self.current_job,self.current_text,))
            cur.execute("DELETE FROM results WHERE unique_id = ?",(self.unique_id,))
        self.__get_next_result()

    def __no_results_jobs_handler(self):
        if self.current_uid is None:
            self.ideal_button.setEnabled(False)
            self.good_button.setEnabled(False)
            self.neutral_button.setEnabled(False)
            self.bad_button.setEnabled(False)
            self.ignore_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.catagory_container.setEnabled(False)
            self.open_job_link_button.setEnabled(False)
            self.skip_job_button.setEnabled(False)

            self.job_desc_text.setText("No results found.")

    def __setup_text_info_containers(self):
        self.instructions_container = QtWidgets.QGroupBox(self.hold_frame)
        self.instructions_container.setGeometry(QtCore.QRect(10, 10, 891, 111))
        self.instructions_container.setTitle("")
        self.instructions_container.setObjectName("instructions_container")
        self.instructions_text = QtWidgets.QTextBrowser(self.instructions_container)
        self.instructions_text.setGeometry(QtCore.QRect(10, 10, 871, 91))
        self.instructions_text.setObjectName("instructions_text")
        self.main_container = QtWidgets.QGroupBox(self.hold_frame)
        self.main_container.setGeometry(QtCore.QRect(10, 10, 891, 791))
        self.main_container.setTitle("")
        self.main_container.setFlat(True)
        self.main_container.setObjectName("main_container")

        self.job_desc_container = QtWidgets.QGroupBox(self.main_container)
        self.job_desc_container.setGeometry(QtCore.QRect(0, 120, 751, 671))
        self.job_desc_container.setTitle("")
        self.job_desc_container.setFlat(False)
        self.job_desc_container.setObjectName("job_desc_container")
        self.job_desc_text = QtWidgets.QTextBrowser(self.job_desc_container)
        self.job_desc_text.setGeometry(QtCore.QRect(10, 10, 731, 651))
        self.job_desc_text.setFrameShape(QtWidgets.QFrame.Panel)
        self.job_desc_text.setFrameShadow(QtWidgets.QFrame.Plain)
        self.job_desc_text.setObjectName("job_desc_text")
        self.location_container = QtWidgets.QGroupBox(self.main_container)
        self.location_container.setGeometry(QtCore.QRect(760, 260, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.location_container.setFont(font)
        self.location_container.setAlignment(QtCore.Qt.AlignCenter)
        self.location_container.setFlat(True)
        self.location_container.setObjectName("location_container")
        self.location_info = QtWidgets.QTextBrowser(self.location_container)
        self.location_info.setGeometry(QtCore.QRect(0, 20, 131, 21))
        self.location_info.setFrameShape(QtWidgets.QFrame.Box)
        self.location_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.location_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.location_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.location_info.setObjectName("location_info")
        self.company_container = QtWidgets.QGroupBox(self.main_container)
        self.company_container.setGeometry(QtCore.QRect(760, 190, 131, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.company_container.setFont(font)
        self.company_container.setAlignment(QtCore.Qt.AlignCenter)
        self.company_container.setFlat(True)
        self.company_container.setObjectName("company_container")
        self.company_info = QtWidgets.QTextBrowser(self.company_container)
        self.company_info.setGeometry(QtCore.QRect(0, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.company_info.setFont(font)
        self.company_info.setFrameShape(QtWidgets.QFrame.Box)
        self.company_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.company_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.company_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.company_info.setObjectName("company_info")
        self.jobtitle_container = QtWidgets.QGroupBox(self.main_container)
        self.jobtitle_container.setGeometry(QtCore.QRect(760, 120, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.jobtitle_container.setFont(font)
        self.jobtitle_container.setAlignment(QtCore.Qt.AlignCenter)
        self.jobtitle_container.setFlat(True)
        self.jobtitle_container.setObjectName("jobtitle_container")
        self.jobtitle_info = QtWidgets.QTextBrowser(self.jobtitle_container)
        self.jobtitle_info.setGeometry(QtCore.QRect(0, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.jobtitle_info.setFont(font)
        self.jobtitle_info.setFrameShape(QtWidgets.QFrame.Box)
        self.jobtitle_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.jobtitle_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.jobtitle_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.jobtitle_info.setObjectName("jobtitle_info")

    def __setup_catagory_buttons(self):
        self.catagory_container = QtWidgets.QGroupBox(self.main_container)
        self.catagory_container.setGeometry(QtCore.QRect(760, 340, 131, 251))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.catagory_container.setFont(font)
        self.catagory_container.setAutoFillBackground(True)
        self.catagory_container.setStyleSheet("_QGroupBox{background-color : rgb(255, 255, 255);}")
        self.catagory_container.setAlignment(QtCore.Qt.AlignCenter)
        self.catagory_container.setFlat(True)
        self.catagory_container.setObjectName("catagory_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.catagory_container)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ideal_button = QtWidgets.QPushButton(self.catagory_container)
        if True:
            palette = QtGui.QPalette()
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(250, 248, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(208, 191, 247))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(83, 67, 120))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(111, 89, 160))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(211, 194, 247))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(250, 248, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(208, 191, 247))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(83, 67, 120))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(111, 89, 160))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(211, 194, 247))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
            brush = QtGui.QBrush(QtGui.QColor(250, 248, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
            brush = QtGui.QBrush(QtGui.QColor(208, 191, 247))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
            brush = QtGui.QBrush(QtGui.QColor(83, 67, 120))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
            brush = QtGui.QBrush(QtGui.QColor(111, 89, 160))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
            brush = QtGui.QBrush(QtGui.QColor(167, 134, 240))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            brush.setStyle(QtCore.Qt.SolidPattern)
            palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)

        self.ideal_button.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ideal_button.setFont(font)
        self.ideal_button.setAutoFillBackground(False)
        self.ideal_button.setStyleSheet(
            "QPushButton {font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Yellow;font-weight: bold;}\n"
            "")
        self.ideal_button.setFlat(False)
        self.ideal_button.setObjectName("ideal_button")
        self.verticalLayout.addWidget(self.ideal_button)
        self.good_button = QtWidgets.QPushButton(self.catagory_container)
        self.good_button.setStyleSheet(
            "QPushButton {font: 75 12pt \"MS Shell Dlg 2\"; font-weight: bold;color: Green;}\n"
            "")
        self.good_button.setObjectName("good_button")
        self.verticalLayout.addWidget(self.good_button)
        self.neutral_button = QtWidgets.QPushButton(self.catagory_container)
        self.neutral_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";font-weight: bold;color:Black;")
        self.neutral_button.setObjectName("neutral_button")
        self.verticalLayout.addWidget(self.neutral_button)
        self.bad_button = QtWidgets.QPushButton(self.catagory_container)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.bad_button.setFont(font)
        self.bad_button.setAutoFillBackground(False)
        self.bad_button.setStyleSheet("QPushButton {font: 12pt \"MS Shell Dlg 2\"; color: Red;font-weight: bold;}\\n")
        self.bad_button.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Switzerland))
        self.bad_button.setObjectName("bad_button")
        self.verticalLayout.addWidget(self.bad_button)
        self.ignore_button = QtWidgets.QPushButton(self.catagory_container)
        self.ignore_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;")
        self.ignore_button.setObjectName("ignore_button")
        self.verticalLayout.addWidget(self.ignore_button)

        self.neutral_button.clicked.connect(lambda b=self.neutral_button :
                                        self.__button_click_response_handler(self.neutral_button))
        self.ideal_button.clicked.connect(lambda b=self.ideal_button :
                                        self.__button_click_response_handler(self.ideal_button))
        self.bad_button.clicked.connect(lambda b=self.bad_button :
                                        self.__button_click_response_handler(self.bad_button))
        self.good_button.clicked.connect(lambda b=self.good_button :
                                        self.__button_click_response_handler(self.good_button))
        self.ignore_button.clicked.connect(lambda b=self.ignore_button :
                                        self.__button_click_response_handler(self.ignore_button))

    def __setup_options_buttons(self):

        self.options_container = QtWidgets.QGroupBox(self.main_container)
        self.options_container.setGeometry(QtCore.QRect(760, 600, 131, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.options_container.setFont(font)
        self.options_container.setAutoFillBackground(True)
        self.options_container.setStyleSheet("_QGroupBox{background-color : rgb(255, 255, 255);}")
        self.options_container.setAlignment(QtCore.Qt.AlignCenter)
        self.options_container.setFlat(True)
        self.options_container.setObjectName("options_container")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.options_container)
        self.gridLayout_2.setObjectName("training_data_layout")
        self.exit_button = QtWidgets.QPushButton(self.options_container)
        self.exit_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;")
        self.exit_button.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.exit_button.setObjectName("exit_button")
        self.gridLayout_2.addWidget(self.exit_button, 3, 0, 1, 1)
        self.next_button = QtWidgets.QPushButton(self.options_container)
        self.next_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;")
        self.next_button.setObjectName("next_button")
        self.gridLayout_2.addWidget(self.next_button, 1, 0, 1, 1)
        self.skip_job_button = QtWidgets.QPushButton(self.options_container)
        self.skip_job_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;")
        self.skip_job_button.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.skip_job_button.setObjectName("skip_job_button")
        self.gridLayout_2.addWidget(self.skip_job_button, 2, 0, 1, 1)
        self.open_job_link_button = QtWidgets.QPushButton(self.options_container)
        self.open_job_link_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;font-weight: bold;")
        self.open_job_link_button.setObjectName("open_job_link_button")
        self.gridLayout_2.addWidget(self.open_job_link_button, 0, 0, 1, 1)

        self.skip_job_button.clicked.connect(lambda : self.__get_next_result())

        self.exit_button.clicked.connect(lambda : self.MainWindow.close())
        self.open_job_link_button.clicked.connect(lambda : webbrowser.open(self.link))
        self.next_button.clicked.connect(lambda b = self.ignore_button : self.__button_click_response_handler(self.ignore_button))

    def setupUi(self):
        MainWindow = self.MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 830)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.hold_frame = QtWidgets.QFrame(self.centralwidget)
        self.hold_frame.setGeometry(QtCore.QRect(10, 10, 911, 811))
        self.hold_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.hold_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.hold_frame.setObjectName("hold_frame")

        self.__setup_text_info_containers()
        self.__setup_options_buttons()

        self.__setup_catagory_buttons()

        self.catagory_container.raise_()
        self.options_container.raise_()
        self.location_container.raise_()
        self.company_container.raise_()
        self.jobtitle_container.raise_()
        self.job_desc_container.raise_()
        self.main_container.raise_()
        self.instructions_container.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.exit_button, self.instructions_text)
        MainWindow.setTabOrder(self.instructions_text, self.next_button)
        MainWindow.setTabOrder(self.next_button, self.ideal_button)
        MainWindow.setTabOrder(self.ideal_button, self.good_button)
        MainWindow.setTabOrder(self.good_button, self.neutral_button)
        MainWindow.setTabOrder(self.neutral_button, self.bad_button)
        MainWindow.setTabOrder(self.bad_button, self.ignore_button)
        MainWindow.setTabOrder(self.ignore_button, self.skip_job_button)
        MainWindow.setTabOrder(self.skip_job_button, self.open_job_link_button)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.instructions_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.5pt;\">Instructions : This window contains the results of the classification model running. To get to the webpage for a given job, just click the </span><span style=\" font-size:9.5pt; font-weight:600;\">Go To Job</span><span style=\" font-size:9.5pt;\"> button and you will be taken there. Once you are done with a job, you can either click Next to move onto the next job, or use one of the buttons in \'Catagories\' to add the job to the training data for this search. Note that doing either of these will remove the job from future viewings, if you would like to come back to this job later, just click skip and it will show up the next time you view results for this term.</span></p></body></html>"))
        self.catagory_container.setTitle(_translate("MainWindow", "Catagories"))
        self.ideal_button.setToolTip(_translate("MainWindow", "Use for jobs that are a perfect fit for your qualifications and requirements"))
        self.ideal_button.setText(_translate("MainWindow", "Ideal"))
        self.good_button.setToolTip(_translate("MainWindow", "Use for jobs related to the search term that are near ideal but not a complete match to your requirments or qualifications"))
        self.good_button.setText(_translate("MainWindow", "Good"))
        self.neutral_button.setToolTip(_translate("MainWindow", "Use for jobs related to the search term that you would consider applying for, but do not meet many of your qualifications or job requirments"))
        self.neutral_button.setText(_translate("MainWindow", "Neutral"))
        self.bad_button.setToolTip(_translate("MainWindow", "Use for jobs that are related to the search term but are far outside of your consideration (i.e. too much/little experience required, unmet requirments, etc.)."))
        self.bad_button.setText(_translate("MainWindow", "Bad"))
        self.ignore_button.setToolTip(_translate("MainWindow", "Ignore current job when training models. Should be used for jobs you are unsure how to catagorize, or ones that have nothing to do with your search."))
        self.ignore_button.setText(_translate("MainWindow", "Ignore"))
        self.options_container.setTitle(_translate("MainWindow", "Options"))
        self.exit_button.setToolTip(_translate("MainWindow", "Leave remaining jobs unsorted and close the window"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.next_button.setToolTip(_translate("MainWindow", "Leave current job unsorted and move on to the next."))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.skip_job_button.setToolTip(_translate("MainWindow", "Leave remaining jobs unsorted and close the window"))
        self.skip_job_button.setText(_translate("MainWindow", "Skip"))
        self.open_job_link_button.setToolTip(_translate("MainWindow", "Leave current job unsorted and move on to the next."))
        self.open_job_link_button.setText(_translate("MainWindow", "Go to Job"))
        self.job_desc_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">CNC Programmer Machinist</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Bent River Machine, Inc.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">- Clarkdale, AZ 86324</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Bent River Machine is seeking a CNC Programmer Machinist responsible for developing the program code to machine parts based on the blueprint along with optimizing the programs to achieve better efficiency. The CNC Programmer Machinist works independently with little direct supervision in the maintenance of assigned systems and the development and installation of systems of moderate size/complexity.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Current CAM software is FeatureCam, previous experience not required but preferable that this software is known or can be quickly learned.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">RESPONSIBILITIES</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Create process plans and programs on time and within budget</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">High level of operational support for mutual success – promote a team environment</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Review customer requirements and incorporate within processes</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Analyze drawings, computer models and design data to correctly calculate part dimensions for machines, tool selection, machine speeds, feed rates and efficient tool path development</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Facilitate the flow of work and resource requirements within the shop floor to meet job requirements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Maximize manufacturing performance on all assigned products</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Design work holding fixtures</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Produce CNC programs with minimal errors</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Check and release all produced CNC programs to prevent crashes</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Inspect parts for compliance upon execution of programs.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Research and implement techniques to increase machine run time</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Communicate recommendations to modify processes to improve productivity and quality</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Complete required records and time scan-in and scan-out of billable jobs</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Observe and contribute during machine set-ups and optimize processes</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Recommend tool purchases and maintain current tools</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Perform routine preventive maintenance on assigned equipment</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Assist and participate in continuous improvements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Adhere to company safety requirements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Comply with company ISO/Quality Management System requirements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Work as a fabrication team to meet operational quality objectives and metrics: on time to promise, quality, product yield, and hours completed</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Support Quoting Lead by providing machining times and blank material sizes.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">JOB REQUIREMENTS</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Significant experience: CAD/CAM, FeatureCam, Esprit, NX, Mastercam, Gibbs, Solidworks, etc. Experience in any or all programs</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Great problem solving skills and the ability to handle simultaneous projects</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Process planning experience including shop routings, set-up sheets, tool lists, bills of material, assembly instructions and process sequences</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Must have knowledge of the latest tools available and be able to research and implement for best optimal performance</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Knowledge in assembly, machining, good machining practices, feeds and speeds, ability to read and understand drawings, quality control and safety.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Experience working in a lean manufacturing or continuous improvement environment</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Self-motivated and capable of working with minimal supervision</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Ability to lift 75lbs.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">COMPENSATION</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">This is a full time, hourly position with compensation based on experience. Full time employees are eligible for benefits after 90 days of employment. This includes holiday pay, vacation/paid time off, health insurance, dental insurance, long term disability, IRA program with percentage match contributions, and educational opportunities for skill set development.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Job Type: Full-time</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">Experience:</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">CNC Programming on CAM/CAD Software: 5 years (Required)</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\">n/a</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2,sans-serif\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p></body></html>"))
        self.location_container.setTitle(_translate("MainWindow", "Location"))
        self.location_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt;\">Grosse Ile, MI</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;\"><br /></p></body></html>"))
        self.company_container.setTitle(_translate("MainWindow", "Company"))
        self.company_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;\"><br /></p></body></html>"))
        self.jobtitle_container.setTitle(_translate("MainWindow", "Job Title"))
        self.jobtitle_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;\"><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ResultsWindow(MainWindow, '../Chemical Engineer')

    MainWindow.show()
    sys.exit(app.exec_())

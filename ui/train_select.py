import os
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets

from ui import SCALE_FACTOR

class TrainSelectWindow(object):

    def __init__(self,window_obj,file_term):
        self.MainWindow = window_obj
        self.file_term = file_term
        self.database = sqlite3.connect(os.path.join(os.getcwd(),file_term,f'{file_term}.db'))
        self.current_unique_id = None
        self.current_job = None
        self.current_text = None
        self.closed = False


        with self.database:
            cur = self.database.cursor()
            self.unsorted_jobs = cur.execute("SELECT * from unsorted").fetchall()
            self.unsorted_jobs.append(None)

        self.setupUi()
        if self.unsorted_jobs[0] is not None:
            self.__get_next_job()
        else:
            self.__no_unsorted_jobs_handler()

    def __exit(self):
        self.closed = True
        self.MainWindow.close()
    def __get_next_job(self):
        nextuns = self.unsorted_jobs.pop(0)
        if nextuns is not None:
            self.current_unique_id, self.current_job, self.current_text = nextuns
            self.job_desc_text.setText(self.current_text)
        else:
            self.MainWindow.close()

    def __button_click_response_handler(self,button):
        response = button.text()+" Jobs"
        with self.database:
            cur = self.database.execute("INSERT INTO training VALUES(?,?,?,?)",
                                        (self.current_unique_id, response, self.current_job, self.current_text,))
            cur.execute("DELETE FROM unsorted WHERE unique_id = ?", (self.current_unique_id,))
        self.__get_next_job()

    def __no_unsorted_jobs_handler(self):
        if self.current_uid == None:
            self.ideal_button.setEnabled(False)
            self.good_button.setEnabled(False)
            self.neutral_button.setEnabled(False)
            self.bad_button.setEnabled(False)
            self.ignore_button.setEnabled(False)
            self.next_button.setEnabled(False)
            self.catagory_container.setEnabled(False)
            self.job_desc_text.setText("No unsorted jobs found. To get new jobs, go to the Search tab and run a search"
                                       "for the job type you want to create training models for.")
    def __setup_options_container(self):
        self.options_container = QtWidgets.QGroupBox(self.hold_frame)
        self.options_container.setGeometry(QtCore.QRect(770, 640, 121, 141))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.options_container.setFont(font)
        self.options_container.setAutoFillBackground(True)
        self.options_container.setStyleSheet("_QGroupBox{background-color : rgb(255, 255, 255);}")
        self.options_container.setAlignment(QtCore.Qt.AlignCenter)
        self.options_container.setObjectName("options_container")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.options_container)
        self.gridLayout_2.setObjectName("training_data_layout")
        self.next_button = QtWidgets.QPushButton(self.options_container)
        self.next_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;")
        self.next_button.setObjectName("next_button")
        self.gridLayout_2.addWidget(self.next_button, 1, 0, 1, 1)
        self.exit_button = QtWidgets.QPushButton(self.options_container)
        self.exit_button.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";color:Black;")
        self.exit_button.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.exit_button.setObjectName("exit_button")
        self.gridLayout_2.addWidget(self.exit_button, 2, 0, 1, 1)

        self.next_button.clicked.connect(self.__get_next_job)
        self.exit_button.clicked.connect(self.__exit)

    def __setup_text_containers(self):
        self.instructions_container = QtWidgets.QGroupBox(self.hold_frame)
        self.instructions_container.setGeometry(QtCore.QRect(10, 10, 891, 111))
        self.instructions_container.setTitle("")
        self.instructions_container.setObjectName("instructions_container")
        self.instructions_text = QtWidgets.QTextBrowser(self.instructions_container)
        self.instructions_text.setGeometry(QtCore.QRect(10, 10, 871, 91))
        self.instructions_text.setObjectName("instructions_text")
        self.job_desc_text = QtWidgets.QTextBrowser(self.hold_frame)
        self.job_desc_text.setGeometry(QtCore.QRect(20, 130, 741, 651))
        self.job_desc_text.setObjectName("job_desc_text")
        self.groupBox = QtWidgets.QGroupBox(self.hold_frame)
        self.groupBox.setGeometry(QtCore.QRect(10, 120, 891, 671))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

    def __setup_label_container(self):
        self.catagory_container = QtWidgets.QGroupBox(self.groupBox)
        self.catagory_container.setGeometry(QtCore.QRect(760, 10, 121, 321))

        font = QtGui.QFont()
        font.setPointSize(12)
        self.catagory_container.setFont(font)
        self.catagory_container.setAutoFillBackground(True)
        self.catagory_container.setStyleSheet("_QGroupBox :enabled {background-color : rgb(255, 255, 255);} :disbaled {color : Grey;background-color : Grey;}")
        self.catagory_container.setAutoFillBackground(True)
        self.catagory_container.setAlignment(QtCore.Qt.AlignCenter)
        self.catagory_container.setObjectName("catagory_container")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.catagory_container)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ideal_button = QtWidgets.QPushButton(self.catagory_container)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ideal_button.setFont(font)
        self.ideal_button.setAutoFillBackground(False)
        self.ideal_button.setStyleSheet(
            "QPushButton {font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: #CCCC00	;font-weight: bold;}")
        self.ideal_button.setFlat(False)
        self.ideal_button.setObjectName("ideal_button")


        self.verticalLayout.addWidget(self.ideal_button)
        self.good_button = QtWidgets.QPushButton(self.catagory_container)
        self.good_button.setStyleSheet(
            "QPushButton {font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Green;font-weight: bold;}"
      )
        self.good_button.setObjectName("good_button")


        self.verticalLayout.addWidget(self.good_button)
        self.neutral_button = QtWidgets.QPushButton(self.catagory_container)
        self.neutral_button.setStyleSheet("QPushButton {font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Black;font-weight: bold;}")
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
        self.bad_button.setStyleSheet("QPushButton {font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Red;font-weight: bold;}")
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
    def setupUi(self):
        MainWindow = self.MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(931, 822)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.hold_frame = QtWidgets.QFrame(self.centralwidget)
        self.hold_frame.setGeometry(QtCore.QRect(10, 9, 911, 801))
        self.hold_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.hold_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.hold_frame.setObjectName("hold_frame")

        self.__setup_options_container()
        self.__setup_text_containers()
        self.__setup_label_container()

        self.instructions_container.raise_()
        self.groupBox.raise_()
        self.options_container.raise_()
        self.job_desc_text.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.options_container.setTitle(_translate("MainWindow", "Options"))
        self.next_button.setToolTip(_translate("MainWindow", "Leave current job unsorted and move on to the next."))
        self.next_button.setText(_translate("MainWindow", "Next"))
        self.exit_button.setToolTip(_translate("MainWindow", "Leave remaining jobs unsorted and close the window"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.instructions_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.5pt;\">Instructions : Sort each job description by using either the Ideal,Good,Neutral, or Bad buttons, </span><span style=\" font-size:9.5pt; text-decoration: underline;\">or use the Ignore button if the job is completely unrelated to your search</span><span style=\" font-size:9.5pt;\"> (i.e. a chemical engineering job from an electrical engineering search term). If you want to come back to this job later use the Next button, and if you want to stop sorting for now, use the Exit Button.</span></p></body></html>"))
        self.job_desc_text.setHtml(_translate("MainWindow", """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" 
        "http://www.w3.org/TR/REC-html40/strict.dtd"> <html><head><meta name="qrichtext" content="1" /><style 
        type="text/css"> p, li { white-space: pre-wrap; } </style></head><body style=" font-family:'MS Shell Dlg 2'; 
        font-size:12pt; font-weight:400; font-style:normal;"> <p style="-qt-paragraph-type:empty; margin-top:0px; 
        margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p> <p 
        style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; 
        text-indent:0px;"><span style=" font-family:'MS Shell Dlg 2,sans-serif'; font-size:10pt;"> </span><span 
        style=" font-size:10pt;"> </span></p></body></html>))"""))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)



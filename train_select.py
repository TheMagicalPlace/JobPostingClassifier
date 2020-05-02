# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'job_select_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3,os

class TrainSelectWindow(object):

    def __init__(self,window_obj,file_term):
        self.MainWindow = window_obj
        self.file_term = file_term
        self.database = sqlite3.connect(os.path.join(os.getcwd(),file_term,f'{file_term}.db'))
        self.current_uid = None
        self.current_job = None
        self.current_text = None

        self.setupUi()
        with self.database:
            cur = self.database.cursor()
            self.unsorted_jobs = cur.execute("SELECT * from unsorted").fetchall()
            self.unsorted_jobs.append(None)


        if self.unsorted_jobs[0] is not None:
            self.__get_next_job()
        else:
            self.__no_unsorted_jobs_handler()

    def __get_next_job(self):
        nextuns = self.unsorted_jobs.pop()
        if nextuns is not None:

            self.unique_id,self.current_job,self.current_text = nextuns
            self.job_desc_text.setText(self.current_text)
        else:
            self.MainWindow.close()

    def __button_click_response_handler(self,button):
        response = button.text()+" Jobs"
        with self.database:
            cur = self.database.execute("INSERT INTO training VALUES(?,?,?,?)",
                                        (self.unique_id,response,self.current_job,self.current_text,))
            cur.execute("DELETE FROM unsorted WHERE unique_id = ?",(self.unique_id,))
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
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.exit_button.clicked.connect(lambda : self.MainWindow.close())

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
            "QPushButton :enabled{font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Yellow;font-weight: bold;} "
            ":disabled {color: Yellow;font-weight: normal;}" 
            "")
        self.ideal_button.setFlat(False)
        self.ideal_button.setObjectName("ideal_button")


        self.verticalLayout.addWidget(self.ideal_button)
        self.good_button = QtWidgets.QPushButton(self.catagory_container)
        self.good_button.setStyleSheet(
            "QPushButton :enabled{font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Green;font-weight: bold;} "
            ":disabled {color: Green;font-weight: normal;font: 12pt \"MS Shell Dlg 2\"}"
            "")
        self.good_button.setObjectName("good_button")


        self.verticalLayout.addWidget(self.good_button)
        self.neutral_button = QtWidgets.QPushButton(self.catagory_container)
        self.neutral_button.setStyleSheet("QPushButton :enabled{font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Black;font-weight: bold;} "
            ":disabled {color: Black;font-weight: normal;font: 12pt \"MS Shell Dlg 2\"}"
            "")
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
        self.bad_button.setStyleSheet("QPushButton :enabled{font-weight: bold;font: 12pt \"MS Shell Dlg 2\"; color: Red;font-weight: bold;} "
            ":disabled {color: Red;font-weight: normal;font: 12pt \"MS Shell Dlg 2\"}"
            "")
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
        self.job_desc_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">CNC Programmer Machinist</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Bent River Machine, Inc.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">- Clarkdale, AZ 86324</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Bent River Machine is seeking a CNC Programmer Machinist responsible for developing the program code to machine parts based on the blueprint along with optimizing the programs to achieve better efficiency. The CNC Programmer Machinist works independently with little direct supervision in the maintenance of assigned systems and the development and installation of systems of moderate size/complexity.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Current CAM software is FeatureCam, previous experience not required but preferable that this software is known or can be quickly learned.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">RESPONSIBILITIES</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Create process plans and programs on time and within budget</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">High level of operational support for mutual success – promote a team environment</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Review customer requirements and incorporate within processes</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Analyze drawings, computer models and design data to correctly calculate part dimensions for machines, tool selection, machine speeds, feed rates and efficient tool path development</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Facilitate the flow of work and resource requirements within the shop floor to meet job requirements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Maximize manufacturing performance on all assigned products</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Design work holding fixtures</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Produce CNC programs with minimal errors</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Check and release all produced CNC programs to prevent crashes</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Inspect parts for compliance upon execution of programs.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Research and implement techniques to increase machine run time</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Communicate recommendations to modify processes to improve productivity and quality</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Complete required records and time scan-in and scan-out of billable jobs</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Observe and contribute during machine set-ups and optimize processes</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Recommend tool purchases and maintain current tools</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Perform routine preventive maintenance on assigned equipment</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Assist and participate in continuous improvements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Adhere to company safety requirements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Comply with company ISO/Quality Management System requirements</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Work as a fabrication team to meet operational quality objectives and metrics: on time to promise, quality, product yield, and hours completed</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Support Quoting Lead by providing machining times and blank material sizes.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">JOB REQUIREMENTS</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Significant experience: CAD/CAM, FeatureCam, Esprit, NX, Mastercam, Gibbs, Solidworks, etc. Experience in any or all programs</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Great problem solving skills and the ability to handle simultaneous projects</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Process planning experience including shop routings, set-up sheets, tool lists, bills of material, assembly instructions and process sequences</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Must have knowledge of the latest tools available and be able to research and implement for best optimal performance</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Knowledge in assembly, machining, good machining practices, feeds and speeds, ability to read and understand drawings, quality control and safety.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Experience working in a lean manufacturing or continuous improvement environment</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Self-motivated and capable of working with minimal supervision</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Ability to lift 75lbs.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">COMPENSATION</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">This is a full time, hourly position with compensation based on experience. Full time employees are eligible for benefits after 90 days of employment. This includes holiday pay, vacation/paid time off, health insurance, dental insurance, long term disability, IRA program with percentage match contributions, and educational opportunities for skill set development.</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Job Type: Full-time</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">Experience:</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">CNC Programming on CAM/CAD Software: 5 years (Required)</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\">n/a</span><span style=\" font-size:10pt;\"> </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt;\"> </span><span style=\" font-size:10pt;\"> </span></p></body></html>"))
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



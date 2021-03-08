# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading_programme.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 360)
        Form.setMinimumSize(QtCore.QSize(620, 360))
        Form.setMaximumSize(QtCore.QSize(620, 360))
        Form.setStyleSheet("\n"
"\n"
"/* ############ color 1 ############# */\n"
"QListWidget,#frame_29,#frame_49,#frame_40, QWidget,QTabBar::tab{\n"
"background-color: #f1f1f1 ;\n"
"}\n"
"\n"
"/* ############ color 2 ############# */\n"
"\n"
"#menuBar,#frame_2 ,\n"
"QTabBar::tab:selected, QTabBar::tab:hover ,QHeaderView,\n"
"#frame,#units_frame,#rm_frame,#frame_4{\n"
"\n"
"background-color:#206087;\n"
"\n"
"}\n"
"\n"
"/* ############ color 3 ############# */\n"
"QToolButton:pressed,QPushButton:pressed,QToolTip {\n"
"background-color: #206087;\n"
"\n"
"}\n"
"\n"
"/* ############ color 4 ############# */\n"
"\n"
"QLineEdit , QPushButton , QToolButton , QListWidget , QListWidget::item,QListWidget::item:selected , QPushButton , QSpinBox ,  QComboBox  , QDateEdit\n"
",#frame_7 ,#frame_9,QTextEdit,QProgressBar,QTableView,QToolTip\n"
"{border: 2px solid #419fd9;\n"
"}\n"
"QTableWidget{\n"
"    gridline-color: 2px solid #f1f1f1;\n"
"\n"
"}\n"
"QTableView::item:selected,\n"
"QScrollBar:handle,QListWidget:item:hover,#products_list::item:selected\n"
"{\n"
"background-color: #419fd9 ;\n"
"\n"
"}\n"
"\n"
"/* ############ font color  ############# */\n"
"\n"
"QWidget,QListWidget::item:selected{\n"
"color:rgb(10,10,10);\n"
"\n"
"\n"
"}\n"
"#Form{background-image: url(icons/photo_2021-03-03_20-05-21.jpg);}\n"
"\n"
"QToolButton,QPushButton{\n"
"    background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(50, 50, 50, 0.5));\n"
"}\n"
"#label,#label_6,#label_18,#label_10,#label_14{\n"
"color:rgb(255,255,255);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"/* ############ main tap widget ############# */\n"
"#frame,#frame_2,#frame,#units_frame,#rm_frame,#frame_4{\n"
"border-radius: 10px;}\n"
"\n"
"\n"
"QTabWidget::pane {\n"
"    border-top: 0px solid #C2C7CB;\n"
"}\n"
"QTabWidget::tab-bar {\n"
"    left: 20px;\n"
"margin-left:20px;\n"
"margin-right:20px;\n"
"}\n"
"QTabBar::tab {\n"
"\n"
"    border: 0px solid rgb(0, 0, 0);\n"
"    min-width: 100px;\n"
"    padding: 09px;\n"
"    border-bottom-right-radius: 15px;\n"
"    border-bottom-left-radius: 15px;\n"
"\n"
"}\n"
"#frame_54,QProgressBar,QLineEdit{\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.243781 rgba(62, 62, 62, 0));\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"\n"
"border-bottom-right-radius: 15px;\n"
"border-bottom-left-radius: 15px;\n"
"\n"
"\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected {\n"
"    border: 0px solid rgb(0, 0, 0);\n"
"}\n"
"QTabBar::tab:!selected {\n"
"    margin-bottom: 4px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"    margin-left: -0px;\n"
"    margin-right: -0px;\n"
"}\n"
"\n"
"\n"
"/* ####################### */\n"
"\n"
"QLabel,QCheckBox{\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.243781 rgba(62, 62, 62, 0));\n"
"}\n"
"\n"
"\n"
"QLineEdit , QPushButton , QToolButton , QListWidget::item ,QRadioButton, QPushButton , QSpinBox , QDoubleSpinBox ,  QComboBox  , QDateEdit\n"
",#frame_7 ,#frame_9,QTextEdit,QProgressBar\n"
"{\n"
"padding-left:6px;\n"
"padding-right:6px;\n"
"\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.243781 rgba(62, 62, 62, 0));\n"
"\n"
"border-radius: 4px;\n"
"\n"
"}\n"
"QListWidget,#frame_29,#frame_49,#frame_40\n"
"{padding:6px;\n"
"padding:6px;\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QListWidget:item{\n"
"margin:2;\n"
"}\n"
"QListWidget{\n"
"border-width:0px;\n"
"}\n"
"\n"
"\n"
"QPushButton , QToolButton,QLineEdit,QComboBox,QDateEdit\n"
",QSpinBox{border-radius: 10px;}\n"
"\n"
"\n"
"QComboBox::drop-down {\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QListWidget {\n"
"padding-top:8px;\n"
"\n"
"}\n"
" QPushButton , QToolButton{\n"
"\n"
"padding:0px;\n"
"}\n"
"\n"
"\n"
"\n"
"QScrollBar{\n"
"width:5px;}\n"
"\n"
"\n"
"QScrollBar:hover{\n"
"width:10px;}\n"
"\n"
"\n"
"\n"
"\n"
"QHeaderView::section {\n"
"\n"
"    padding: 4px;\n"
"    border-style: none;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0));\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QTableView QTableCornerButton::section {\n"
"\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0));\n"
"\n"
"\n"
"}\n"
"QTableView {\n"
" border: 0px ;\n"
"    border-width: 10px ;\n"
"}\n"
"\n"
"\n"
"\n"
"QToolTip{\n"
"border-radius: 7px;\n"
"border-width: 1px ;\n"
"}\n"
"\n"
"\n"
"QPushButton , QToolButton{ padding:5px;border-width:2px;}\n"
"\n"
"\n"
"QScrollBar::sub-page ,QScrollBar::add-page{\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 0));}\n"
"\n"
"QScrollBar:vertical{\n"
"width:8px;\n"
"}\n"
"\n"
"QScrollBar:horizontal{\n"
"height:8px;\n"
"}\n"
"\n"
"\n"
"QScrollBar:handle\n"
"{\n"
"\n"
"border-radius: 4px;\n"
"}\n"
" QListWidget::item {\n"
"border-width: 1px;\n"
"height:30px;\n"
"\n"
" }\n"
"QScrollBar::add-line ,QScrollBar::sub-line\n"
"{\n"
"      border: none;\n"
"      background: none;\n"
"      color: none;\n"
"}\n"
"\n"
"#frame,#units_frame,#rm_frame,#frame_4{\n"
"border: 0px solid #f1f1f1;\n"
"\n"
"\n"
"}\n"
"QListView {\n"
"    outline: 0;\n"
"}\n"
"\n"
"")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(130, 209, 130, 47)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setStyleSheet("border-width:0px;")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

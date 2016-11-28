# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analysisResults.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AnalysisResults(QtGui.QWidget):
    def setupUi(self, AnalysisResults):
        AnalysisResults.setObjectName(_fromUtf8("AnalysisResults"))
        AnalysisResults.resize(800, 600)
        self.pushButton = QtGui.QPushButton(AnalysisResults)
        self.pushButton.setGeometry(QtCore.QRect(80, 510, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.scrollArea = QtGui.QScrollArea(AnalysisResults)
        self.scrollArea.setGeometry(QtCore.QRect(120, 120, 561, 241))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 559, 239))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.listView = QtGui.QListView(self.scrollAreaWidgetContents)
        self.listView.setGeometry(QtCore.QRect(0, 0, 561, 241))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtGui.QLabel(AnalysisResults)
        self.label.setGeometry(QtCore.QRect(130, 90, 181, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_3 = QtGui.QPushButton(AnalysisResults)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 510, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label_2 = QtGui.QLabel(AnalysisResults)
        self.label_2.setGeometry(QtCore.QRect(130, 390, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(AnalysisResults)
        self.label_3.setGeometry(QtCore.QRect(260, 390, 101, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_4 = QtGui.QPushButton(AnalysisResults)
        self.pushButton_4.setGeometry(QtCore.QRect(560, 510, 160, 40))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))

        self.retranslateUi(AnalysisResults)
        QtCore.QMetaObject.connectSlotsByName(AnalysisResults)

    def retranslateUi(self, AnalysisResults):
        AnalysisResults.setWindowTitle(_translate("AnalysisResults", "Ramas Home", None))
        self.pushButton.setText(_translate("AnalysisResults", "View Timeline", None))
        self.label.setText(_translate("AnalysisResults", "Scanned Memory Images", None))
        self.pushButton_3.setText(_translate("AnalysisResults", " Querying Interface", None))
        self.label_2.setText(_translate("AnalysisResults", "Analysis Status:", None))
        self.label_3.setText(_translate("AnalysisResults", "Done.", None))
        self.pushButton_4.setText(_translate("AnalysisResults", "Back", None))

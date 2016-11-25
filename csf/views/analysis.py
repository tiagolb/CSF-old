# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analysis.ui'
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

class Ui_Analysis(object):
    def setupUi(self, Analysis):
        Analysis.setObjectName(_fromUtf8("Analysis"))
        Analysis.resize(800, 600)
        self.pushButton = QtGui.QPushButton(Analysis)
        self.pushButton.setGeometry(QtCore.QRect(80, 510, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.scrollArea = QtGui.QScrollArea(Analysis)
        self.scrollArea.setGeometry(QtCore.QRect(120, 120, 561, 241))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 559, 239))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtGui.QLabel(Analysis)
        self.label.setGeometry(QtCore.QRect(130, 90, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_3 = QtGui.QPushButton(Analysis)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 510, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label_2 = QtGui.QLabel(Analysis)
        self.label_2.setGeometry(QtCore.QRect(130, 390, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Analysis)
        self.label_3.setGeometry(QtCore.QRect(260, 390, 101, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(Analysis)
        QtCore.QMetaObject.connectSlotsByName(Analysis)

    def retranslateUi(self, Analysis):
        Analysis.setWindowTitle(_translate("Analysis", "Ramas Home", None))
        self.pushButton.setText(_translate("Analysis", "Analyse", None))
        self.label.setText(_translate("Analysis", "Modules", None))
        self.pushButton_3.setText(_translate("Analysis", "Back", None))
        self.label_2.setText(_translate("Analysis", "Analysis Status:", None))
        self.label_3.setText(_translate("Analysis", "Done.", None))


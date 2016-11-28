# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/analysis.ui'
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

class Ui_Analysis(QtGui.QWidget):
    def setupUi(self, Analysis):
        Analysis.setObjectName(_fromUtf8("Analysis"))
        Analysis.resize(800, 600)
        self.pushButton_3 = QtGui.QPushButton(Analysis)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 510, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.widget = QtGui.QWidget(Analysis)
        self.widget.setGeometry(QtCore.QRect(0, 0, 801, 501))
        self.widget.setObjectName(_fromUtf8("widget"))

        self.retranslateUi(Analysis)
        QtCore.QMetaObject.connectSlotsByName(Analysis)

    def retranslateUi(self, Analysis):
        Analysis.setWindowTitle(_translate("Analysis", "Ramas Home", None))
        self.pushButton_3.setText(_translate("Analysis", "Back", None))

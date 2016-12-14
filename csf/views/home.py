# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/home.ui'
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

class Ui_HomePage(QtGui.QWidget):
    def setupUi(self, HomePage):
        HomePage.setObjectName(_fromUtf8("HomePage"))
        HomePage.resize(800, 600)
        self.pushButton_2 = QtGui.QPushButton(HomePage)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 500, 160, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(HomePage)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 500, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton = QtGui.QPushButton(HomePage)
        self.pushButton.setGeometry(QtCore.QRect(80, 500, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(HomePage)
        self.label.setGeometry(QtCore.QRect(120, 100, 551, 311))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(HomePage)
        QtCore.QMetaObject.connectSlotsByName(HomePage)

    def retranslateUi(self, HomePage):
        HomePage.setWindowTitle(_translate("HomePage", "Ramas Home", None))
        self.pushButton_2.setText(_translate("HomePage", "Open Case", None))
        self.pushButton_3.setText(_translate("HomePage", "Install Modules", None))
        self.pushButton.setText(_translate("HomePage", "New Case", None))
        self.label.setText(_translate("HomePage", "TextLabel", None))

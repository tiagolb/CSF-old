# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createCase.ui'
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

class Ui_CreateCase(QtGui.QWidget):
    def setupUi(self, CreateCase):
        CreateCase.setObjectName(_fromUtf8("CreateCase"))
        CreateCase.resize(800, 600)
        self.pushButton_2 = QtGui.QPushButton(CreateCase)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 500, 160, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(CreateCase)
        self.pushButton.setGeometry(QtCore.QRect(80, 500, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit = QtGui.QLineEdit(CreateCase)
        self.lineEdit.setGeometry(QtCore.QRect(280, 150, 361, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(CreateCase)
        self.lineEdit_2.setGeometry(QtCore.QRect(280, 230, 361, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label = QtGui.QLabel(CreateCase)
        self.label.setGeometry(QtCore.QRect(190, 150, 91, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(CreateCase)
        self.label_2.setGeometry(QtCore.QRect(190, 230, 91, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(CreateCase)
        QtCore.QMetaObject.connectSlotsByName(CreateCase)

    def retranslateUi(self, CreateCase):
        CreateCase.setWindowTitle(_translate("CreateCase", "Ramas Home", None))
        self.pushButton_2.setText(_translate("CreateCase", "Cancel", None))
        self.pushButton.setText(_translate("CreateCase", "Create Case", None))
        self.label.setText(_translate("CreateCase", "Case Name", None))
        self.label_2.setText(_translate("CreateCase", "Description", None))

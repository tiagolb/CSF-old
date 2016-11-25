# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addImage.ui'
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

class Ui_AddImage(QtGui.QWidget):
    def setupUi(self, AddImage):
        AddImage.setObjectName(_fromUtf8("AddImage"))
        AddImage.resize(800, 600)
        self.pushButton_2 = QtGui.QPushButton(AddImage)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 500, 160, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(AddImage)
        self.pushButton.setGeometry(QtCore.QRect(80, 500, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit = QtGui.QLineEdit(AddImage)
        self.lineEdit.setGeometry(QtCore.QRect(280, 150, 361, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(AddImage)
        self.label.setGeometry(QtCore.QRect(90, 150, 191, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(AddImage)
        self.label_2.setGeometry(QtCore.QRect(160, 230, 121, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_3 = QtGui.QPushButton(AddImage)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 310, 181, 29))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.lineEdit_3 = QtGui.QLineEdit(AddImage)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 310, 361, 31))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.dateTimeEdit = QtGui.QDateTimeEdit(AddImage)
        self.dateTimeEdit.setGeometry(QtCore.QRect(280, 230, 194, 29))
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))

        self.retranslateUi(AddImage)
        QtCore.QMetaObject.connectSlotsByName(AddImage)

    def retranslateUi(self, AddImage):
        AddImage.setWindowTitle(_translate("AddImage", "Ramas Home", None))
        self.pushButton_2.setText(_translate("AddImage", "Cancel", None))
        self.pushButton.setText(_translate("AddImage", "Add Image", None))
        self.label.setText(_translate("AddImage", "Memory Image Description", None))
        self.label_2.setText(_translate("AddImage", "Acquisition Date", None))
        self.pushButton_3.setText(_translate("AddImage", "Search Memory Image", None))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/caseManager.ui'
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

class Ui_CaseManager(QtGui.QWidget):
    def setupUi(self, CaseManager):
        CaseManager.setObjectName(_fromUtf8("CaseManager"))
        CaseManager.resize(800, 600)
        self.pushButton_2 = QtGui.QPushButton(CaseManager)
        self.pushButton_2.setGeometry(QtCore.QRect(570, 510, 160, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(CaseManager)
        self.pushButton.setGeometry(QtCore.QRect(80, 510, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.scrollArea = QtGui.QScrollArea(CaseManager)
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
        self.label = QtGui.QLabel(CaseManager)
        self.label.setGeometry(QtCore.QRect(130, 90, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_3 = QtGui.QPushButton(CaseManager)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 510, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label_2 = QtGui.QLabel(CaseManager)
        self.label_2.setGeometry(QtCore.QRect(130, 380, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit = QtGui.QLineEdit(CaseManager)
        self.lineEdit.setGeometry(QtCore.QRect(120, 410, 561, 29))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        self.retranslateUi(CaseManager)
        QtCore.QMetaObject.connectSlotsByName(CaseManager)

    def retranslateUi(self, CaseManager):
        CaseManager.setWindowTitle(_translate("CaseManager", "Ramas Home", None))
        self.pushButton_2.setText(_translate("CaseManager", "Back", None))
        self.pushButton.setText(_translate("CaseManager", "Open Case", None))
        self.label.setText(_translate("CaseManager", "Cases", None))
        self.pushButton_3.setText(_translate("CaseManager", "Delete Case", None))
        self.label_2.setText(_translate("CaseManager", "Case Description", None))

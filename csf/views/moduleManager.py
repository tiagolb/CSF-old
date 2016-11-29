# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/moduleManager.ui'
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

class Ui_ModuleManager(QtGui.QWidget):
    def setupUi(self, ModuleManager):
        ModuleManager.setObjectName(_fromUtf8("ModuleManager"))
        ModuleManager.resize(800, 600)
        self.pushButton = QtGui.QPushButton(ModuleManager)
        self.pushButton.setGeometry(QtCore.QRect(50, 500, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(ModuleManager)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 500, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(ModuleManager)
        self.pushButton_4.setGeometry(QtCore.QRect(590, 500, 160, 40))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.lineEdit_2 = QtGui.QLineEdit(ModuleManager)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 330, 731, 29))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_3 = QtGui.QLabel(ModuleManager)
        self.label_3.setGeometry(QtCore.QRect(50, 310, 131, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_5 = QtGui.QLabel(ModuleManager)
        self.label_5.setGeometry(QtCore.QRect(60, 90, 121, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.scrollArea_2 = QtGui.QScrollArea(ModuleManager)
        self.scrollArea_2.setGeometry(QtCore.QRect(40, 120, 731, 171))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 729, 169))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.listView_2 = QtGui.QListView(self.scrollAreaWidgetContents_2)
        self.listView_2.setGeometry(QtCore.QRect(0, 0, 731, 171))
        self.listView_2.setObjectName(_fromUtf8("listView_2"))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.lineEdit_3 = QtGui.QLineEdit(ModuleManager)
        self.lineEdit_3.setGeometry(QtCore.QRect(230, 400, 361, 31))
        self.lineEdit_3.setText(_fromUtf8(""))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.pushButton_5 = QtGui.QPushButton(ModuleManager)
        self.pushButton_5.setGeometry(QtCore.QRect(40, 400, 181, 29))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        self.retranslateUi(ModuleManager)
        QtCore.QMetaObject.connectSlotsByName(ModuleManager)

    def retranslateUi(self, ModuleManager):
        ModuleManager.setWindowTitle(_translate("ModuleManager", "Ramas Home", None))
        self.pushButton.setText(_translate("ModuleManager", "Add Module", None))
        self.pushButton_3.setText(_translate("ModuleManager", "Delete Module", None))
        self.pushButton_4.setText(_translate("ModuleManager", "Back", None))
        self.label_3.setText(_translate("ModuleManager", "Description", None))
        self.label_5.setText(_translate("ModuleManager", "Installed Modules", None))
        self.pushButton_5.setText(_translate("ModuleManager", "Search Module File", None))

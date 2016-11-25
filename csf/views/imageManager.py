# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imageManager.ui'
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

class Ui_ImageManager(QtGui.QWidget):
    def setupUi(self, ImageManager):
        ImageManager.setObjectName(_fromUtf8("ImageManager"))
        ImageManager.resize(800, 600)
        self.pushButton_2 = QtGui.QPushButton(ImageManager)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 510, 160, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(ImageManager)
        self.pushButton.setGeometry(QtCore.QRect(20, 510, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.scrollArea = QtGui.QScrollArea(ImageManager)
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
        self.label = QtGui.QLabel(ImageManager)
        self.label.setGeometry(QtCore.QRect(130, 90, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_3 = QtGui.QPushButton(ImageManager)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 510, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(ImageManager)
        self.pushButton_4.setGeometry(QtCore.QRect(620, 510, 160, 40))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))

        self.retranslateUi(ImageManager)
        QtCore.QMetaObject.connectSlotsByName(ImageManager)

    def retranslateUi(self, ImageManager):
        ImageManager.setWindowTitle(_translate("ImageManager", "Ramas Home", None))
        self.pushButton_2.setText(_translate("ImageManager", "Analyse", None))
        self.pushButton.setText(_translate("ImageManager", "Add Image", None))
        self.label.setText(_translate("ImageManager", "Memory Images", None))
        self.pushButton_3.setText(_translate("ImageManager", "Delete Image", None))
        self.pushButton_4.setText(_translate("ImageManager", "Back", None))

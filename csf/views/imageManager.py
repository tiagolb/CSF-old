# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/imageManager.ui'
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
        self.pushButton_2.setGeometry(QtCore.QRect(330, 500, 160, 40))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(ImageManager)
        self.pushButton.setGeometry(QtCore.QRect(50, 500, 160, 40))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.scrollArea = QtGui.QScrollArea(ImageManager)
        self.scrollArea.setGeometry(QtCore.QRect(120, 120, 391, 171))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 389, 169))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.listView = QtGui.QListView(self.scrollAreaWidgetContents)
        self.listView.setGeometry(QtCore.QRect(0, 0, 391, 171))
        self.listView.setObjectName(_fromUtf8("listView"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label = QtGui.QLabel(ImageManager)
        self.label.setGeometry(QtCore.QRect(130, 90, 121, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton_3 = QtGui.QPushButton(ImageManager)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 550, 160, 40))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(ImageManager)
        self.pushButton_4.setGeometry(QtCore.QRect(590, 500, 160, 40))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.lineEdit = QtGui.QLineEdit(ImageManager)
        self.lineEdit.setGeometry(QtCore.QRect(120, 330, 561, 29))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(ImageManager)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 390, 561, 29))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_3 = QtGui.QLineEdit(ImageManager)
        self.lineEdit_3.setGeometry(QtCore.QRect(120, 450, 561, 29))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label_2 = QtGui.QLabel(ImageManager)
        self.label_2.setGeometry(QtCore.QRect(130, 310, 131, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(ImageManager)
        self.label_3.setGeometry(QtCore.QRect(130, 370, 131, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(ImageManager)
        self.label_4.setGeometry(QtCore.QRect(130, 430, 131, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(ImageManager)
        self.label_5.setGeometry(QtCore.QRect(550, 90, 121, 17))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.scrollArea_2 = QtGui.QScrollArea(ImageManager)
        self.scrollArea_2.setGeometry(QtCore.QRect(540, 120, 231, 171))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 229, 169))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.listView_2 = QtGui.QListView(self.scrollAreaWidgetContents_2)
        self.listView_2.setGeometry(QtCore.QRect(0, 0, 231, 171))
        self.listView_2.setObjectName(_fromUtf8("listView_2"))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.pushButton_5 = QtGui.QPushButton(ImageManager)
        self.pushButton_5.setGeometry(QtCore.QRect(330, 550, 160, 40))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        self.retranslateUi(ImageManager)
        QtCore.QMetaObject.connectSlotsByName(ImageManager)

    def retranslateUi(self, ImageManager):
        ImageManager.setWindowTitle(_translate("ImageManager", "Ramas Home", None))
        self.pushButton_2.setText(_translate("ImageManager", "Analyse", None))
        self.pushButton.setText(_translate("ImageManager", "Add Image", None))
        self.label.setText(_translate("ImageManager", "Memory Images", None))
        self.pushButton_3.setText(_translate("ImageManager", "Delete Image", None))
        self.pushButton_4.setText(_translate("ImageManager", "Back", None))
        self.label_2.setText(_translate("ImageManager", "Image MD5 Hash", None))
        self.label_3.setText(_translate("ImageManager", "Description", None))
        self.label_4.setText(_translate("ImageManager", "Acquisition Date", None))
        self.label_5.setText(_translate("ImageManager", "Modules", None))
        self.pushButton_5.setText(_translate("ImageManager", "Check Results", None))

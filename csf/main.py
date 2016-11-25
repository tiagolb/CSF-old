import sys, os
from PyQt4 import QtGui, QtCore
import sqlite3 as lite

from dbSchema import initDatabase
from views.home import Ui_HomePage
from views.createCase import Ui_CreateCase
from views.caseManager import Ui_CaseManager
from views.imageManager import Ui_ImageManager
from views.addImage import Ui_AddImage

from models.caseModel import CaseModel
from models.imageModel import ImageModel

dbName = 'ramas.db'

class MainWindow(QtGui.QMainWindow):
    ######################################
    #Setup pages
    ######################################
    def setHomepage(self):
        self.home = Ui_HomePage()
        self.home.setupUi(self.home)
        self.home.pushButton.clicked.connect(self.createCase)
        self.home.pushButton_2.clicked.connect(self.caseManager)
        self.home.pushButton_3.clicked.connect(self.installModules)
        return self.home

    def setCreateCase(self):
        self.createCase = Ui_CreateCase()
        self.createCase.setupUi(self.createCase)
        self.createCase.pushButton.clicked.connect(self.addCase)
        self.createCase.pushButton.setEnabled(False)
        self.createCase.pushButton_2.clicked.connect(self.cancelCaseManager)
        self.createCase.lineEdit.textChanged.connect(self.caseInfoChanged)
        self.createCase.lineEdit_2.textChanged.connect(self.caseInfoChanged)
        return self.createCase

    def setCaseManager(self):
        self.caseManager = Ui_CaseManager()
        self.caseManager.setupUi(self.caseManager)
        self.caseManager.pushButton.clicked.connect(self.manageImages)
        self.caseManager.pushButton_2.clicked.connect(self.cancelCaseManager)
        self.caseManager.pushButton_3.clicked.connect(self.deleteCase)
        self.caseManager.listView.clicked.connect(self.caseSelected)
        self.caseManager.pushButton.setEnabled(False)
        self.caseManager.pushButton_3.setEnabled(False)

        self.caseModel = CaseModel(self.caseManager.listView, self.dbCon)
        self.caseModel.populate()
        self.caseManager.listView.setModel(self.caseModel)
        return self.caseManager

    def setImageManager(self):
        self.imageManager = Ui_ImageManager()
        self.imageManager.setupUi(self.imageManager)
        self.imageManager.listView.clicked.connect(self.imageSelected)
        self.imageManager.pushButton.clicked.connect(self.imageAdding)
        self.imageManager.pushButton_3.setEnabled(False)
        self.imageManager.pushButton_3.clicked.connect(self.deleteImage)
        self.imageManager.pushButton_2.clicked.connect(self.analyse)
        self.imageManager.pushButton_4.clicked.connect(self.cancelImageManager)

        self.imageModel = ImageModel(self.imageManager.listView, self.dbCon)
        self.imageManager.listView.setModel(self.imageModel)
        return self.imageManager

    def setAddImage(self):
        self.imageAddition = Ui_AddImage()
        self.imageAddition.setupUi(self.imageAddition)
        self.imageAddition.pushButton.clicked.connect(self.addImage)
        self.imageAddition.pushButton.setEnabled(False)
        self.imageAddition.pushButton_2.clicked.connect(self.cancelImageManager)
        self.imageAddition.pushButton_3.clicked.connect(self.searchImage)
        self.imageAddition.lineEdit.textChanged.connect(self.imageInfoChanged)
        self.imageAddition.lineEdit_3.textChanged.connect(self.imageInfoChanged)
        self.imageAddition.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        return self.imageAddition
    ######################################
    #Register Callbacks
    ######################################
    def createCase(self):
        self.central_widget.setCurrentWidget(self.createCase)

    def caseSelected(self):
        self.caseManager.pushButton.setEnabled(True)
        self.caseManager.pushButton_3.setEnabled(True)

    def imageSelected(self):
        self.imageManager.pushButton_3.setEnabled(True)

    def caseInfoChanged(self):
        if(len(self.createCase.lineEdit.text()) !=0 and len(self.createCase.lineEdit_2.text()) != 0):
            self.createCase.pushButton.setEnabled(True)
        else:
            self.createCase.pushButton.setEnabled(False)

    def imageInfoChanged(self):
        if(len(self.imageAddition.lineEdit.text()) !=0 and len(self.imageAddition.lineEdit_3.text()) != 0):
            self.imageAddition.pushButton.setEnabled(True)
        else:
            self.imageAddition.pushButton.setEnabled(False)

    def installModules(self):
        print "To be implemented"
        #self.central_widget.setCurrentWidget(self.page)

    def addCase(self):
        #update available cases shown in list
        name = self.createCase.lineEdit.text()
        description = self.createCase.lineEdit_2.text()
        try:
            self.caseModel.insertCase(name, description)
            self.central_widget.setCurrentWidget(self.caseManager)
        except lite.Error, e:
            msg = "A case named \"" + str(name) + "\" already exists."
            reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)



    def imageAdding(self):
        self.central_widget.setCurrentWidget(self.imageAddition)

    def searchImage(self):
        imageLocation = QtGui.QFileDialog.getOpenFileName()
        self.imageAddition.lineEdit_3.setText(imageLocation)

    def addImage(self):
        #get full timestamp in a human readable string
        timestamp = self.imageAddition.dateTimeEdit.dateTime().toPyDateTime()

        if(not os.path.isfile(str(self.imageAddition.lineEdit_3.text()))):
            msg = "File does not exist."
            reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)
        else:
            try:
                self.imageModel.insertImage(str(self.imageAddition.lineEdit_3.text()), self.current_case,
                    self.imageAddition.lineEdit.text(), timestamp)
                self.central_widget.setCurrentWidget(self.imageManager)
            except lite.Error, e:
                msg = "This image file was already added to the case."
                reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)


    def analyse(self):
        #open dialog to select files
        print "analyse"

    def deleteCase(self):
        #Get row index of selected case
        caseIndex = self.caseManager.listView.selectedIndexes()
        del_msg = "Are you sure you want to delete all information pertaining to case " + caseIndex[0].data().toString() + "?"
        reply = QtGui.QMessageBox.warning(self, 'Message', del_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if(reply == QtGui.QMessageBox.Yes):
            self.caseModel.deleteCase(caseIndex[0].row(), caseIndex[0].data().toString())
        else:
            pass

    def deleteImage(self):
        #Get row index of selected image
        imageIndex = self.imageManager.listView.selectedIndexes()
        del_msg = "Are you sure you want to delete all information pertaining to image " + imageIndex[0].data().toString() + "?"
        reply = QtGui.QMessageBox.warning(self, 'Message', del_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if(reply == QtGui.QMessageBox.Yes):
            self.imageModel.deleteImage(imageIndex[0].row(), imageIndex[0].data().toString(), self.current_case)
        else:
            pass


    def caseManager(self):
        self.central_widget.setCurrentWidget(self.caseManager)

    def cancelCaseManager(self):
        self.current_case = "none"
        self.central_widget.setCurrentWidget(self.home)

    def cancelImageManager(self):
        self.central_widget.setCurrentWidget(self.caseManager)

    def manageImages(self):
        caseIndex = self.caseManager.listView.selectedIndexes()
        self.current_case = caseIndex[0].data().toString()
        self.imageModel.populate(self.current_case)
        self.central_widget.setCurrentWidget(self.imageManager)


    def __init__(self):
        super(MainWindow, self).__init__()

        try:
            self.dbCon = lite.connect(dbName)

            initDatabase(self.dbCon)

        except lite.Error, e:
            msg = "Critical error in database. Remove ramas.db and try again."
            reply = QtGui.QMessageBox.critical(self, 'Message', msg, QtGui.QMessageBox.Ok)
            sys.exit(0)

        self.current_case = "none"
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.home = self.setHomepage()
        self.createCase = self.setCreateCase()
        self.imageManager = self.setImageManager()
        self.imageAddition = self.setAddImage()
        self.caseManager = self.setCaseManager()


        self.central_widget.addWidget(self.home)
        self.central_widget.addWidget(self.createCase)
        self.central_widget.addWidget(self.caseManager)
        self.central_widget.addWidget(self.imageManager)
        self.central_widget.addWidget(self.imageAddition)


        self.central_widget.setCurrentWidget(self.home)





def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.setFixedSize(800,600)

    #Move window to screen center
    qr = window.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

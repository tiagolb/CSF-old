import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QUrl
import sqlite3 as lite

from dbSchema import initDatabase
from views.home import Ui_HomePage
from views.createCase import Ui_CreateCase
from views.caseManager import Ui_CaseManager
from views.imageManager import Ui_ImageManager
from views.addImage import Ui_AddImage
from views.analysis import Ui_Analysis

from views.browserWidget import Browser

from models.caseModel import CaseModel
from models.imageModel import ImageModel
from models.moduleModel import ModuleModel

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
        self.caseManager.lineEdit.setReadOnly(True)
        self.caseManager.pushButton.setEnabled(False)
        self.caseManager.pushButton_3.setEnabled(False)

        self.caseModel = CaseModel(self.caseManager.listView, self.dbCon)
        self.caseModel.populate()
        self.caseManager.listView.setModel(self.caseModel)
        self.caseManager.listView.selectionModel().selectionChanged.connect(self.caseSelected)
        return self.caseManager

    def setImageManager(self):
        self.imageManager = Ui_ImageManager()
        self.imageManager.setupUi(self.imageManager)
        self.imageManager.listView.clicked.connect(self.imageSelected)
        self.imageManager.pushButton.clicked.connect(self.imageAdding)
        self.imageManager.pushButton_3.setEnabled(False)
        self.imageManager.pushButton_3.clicked.connect(self.deleteImage)
        self.imageManager.pushButton_2.clicked.connect(self.analyse)
        self.imageManager.pushButton_2.setEnabled(False)
        self.imageManager.pushButton_5.clicked.connect(self.checkResults)
        self.imageManager.pushButton_5.setEnabled(False)
        self.imageManager.pushButton_4.clicked.connect(self.cancelImageManager)
        self.imageManager.lineEdit.setReadOnly(True)
        self.imageManager.lineEdit_2.setReadOnly(True)
        self.imageManager.lineEdit_3.setReadOnly(True)

        self.imageModel = ImageModel(self.imageManager.listView, self.dbCon)
        self.imageManager.listView.setModel(self.imageModel)
        self.imageManager.listView.selectionModel().selectionChanged.connect(self.imageSelected)

        self.moduleModel = ModuleModel(self.imageManager.listView_2, self.dbCon)
        self.moduleModel.populate()
        self.imageManager.listView_2.setModel(self.moduleModel)
        self.imageManager.listView_2.selectionModel().selectionChanged.connect(self.moduleSelected)
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

    def setAnalysis(self):
        self.imageAnalysis = Ui_Analysis()
        self.imageAnalysis.setupUi(self.imageAnalysis)
        return self.imageAnalysis

    ############################################################################
    # HOME SCREEN CALLBACKS
    ############################################################################
    def createCase(self):
        self.central_widget.setCurrentWidget(self.createCase)

    def caseManager(self):
        self.central_widget.setCurrentWidget(self.caseManager)

    def installModules(self):
        print "To be implemented"
        #self.central_widget.setCurrentWidget(self.page)

    ############################################################################
    # NEW CASE CALLBACKS
    ############################################################################
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

    def cancelCaseManager(self):
        self.current_case = "none"
        self.central_widget.setCurrentWidget(self.home)

    def caseInfoChanged(self):
        if(len(self.createCase.lineEdit.text()) !=0 and len(self.createCase.lineEdit_2.text()) != 0):
            self.createCase.pushButton.setEnabled(True)
        else:
            self.createCase.pushButton.setEnabled(False)

    ############################################################################
    # CASE MANAGER CALLBACKS
    ############################################################################
    def manageImages(self):
        caseIndex = self.caseManager.listView.selectedIndexes()
        self.current_case = caseIndex[0].data().toString()
        self.imageModel.populate(self.current_case)
        self.central_widget.setCurrentWidget(self.imageManager)

    def caseSelected(self):
        self.caseManager.pushButton.setEnabled(True)
        self.caseManager.pushButton_3.setEnabled(True)
        caseIndex = self.caseManager.listView.selectedIndexes()
        description = self.caseModel.fetchCaseDescription(caseIndex[0].data().toString())
        self.caseManager.lineEdit.setText(description)

    def deleteCase(self):
        #Get row index of selected case
        caseIndex = self.caseManager.listView.selectedIndexes()
        del_msg = "Are you sure you want to delete all information pertaining to case " + caseIndex[0].data().toString() + "?"
        reply = QtGui.QMessageBox.warning(self, 'Message', del_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if(reply == QtGui.QMessageBox.Yes):
            self.caseModel.deleteCase(caseIndex[0].row(), caseIndex[0].data().toString())
        else:
            pass

    ############################################################################
    # IMAGE MANAGER CALLBACKS
    ############################################################################

    def imageSelected(self):
        self.imageManager.pushButton_2.setEnabled(True)
        self.imageManager.pushButton_3.setEnabled(True)
        imageIndex = self.imageManager.listView.selectedIndexes()
        fileHash, description, date = self.imageModel.fetchImageInfo(imageIndex[0].data().toString(), self.current_case)
        self.imageManager.lineEdit.setText(fileHash)
        self.imageManager.lineEdit_2.setText(description)
        self.imageManager.lineEdit_3.setText(date)

        if(self.imageModel.wasImageAnalysed(fileHash)):
            self.imageManager.pushButton_5.setEnabled(True)
        else:
            self.imageManager.pushButton_5.setEnabled(False)

        self.moduleModel.populateUnprocessedModules(fileHash)


    def checkResults(self):
        self.analysis.widget = Browser()
        #TODO change to show audit file of selected image
        self.analysis.widget.load(QUrl('audit_result/audit.html'))
        self.analysis.widget.show()

    def analyse(self):
        #TODO call analysis of selected Modules
        imageIndex = self.imageManager.listView.selectedIndexes()
        imageLocation = imageIndex[0].data().toString()

        modulesToApply = []
        for index in range(self.moduleModel.rowCount()):
            if(self.moduleModel.item(index).isCheckable()):
                if(self.moduleModel.item(index).checkState()):
                    modulesToApply.append(str(self.moduleModel.item(index).text()))


    def deleteImage(self):
        #Get row index of selected image
        imageIndex = self.imageManager.listView.selectedIndexes()
        del_msg = "Are you sure you want to delete all information pertaining to image " + imageIndex[0].data().toString() + "?"
        reply = QtGui.QMessageBox.warning(self, 'Message', del_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if(reply == QtGui.QMessageBox.Yes):
            self.imageModel.deleteImage(imageIndex[0].row(), imageIndex[0].data().toString(), self.current_case)
        else:
            pass

    def cancelImageManager(self):
        self.central_widget.setCurrentWidget(self.caseManager)
        self.imageManager.lineEdit.clear()
        self.imageManager.lineEdit_2.clear()
        self.imageManager.lineEdit_3.clear()

    def moduleSelected(self):
        pass

    def imageAdding(self):
        self.central_widget.setCurrentWidget(self.imageAddition)

    ############################################################################
    # IMAGE ADDING CALLBACKS
    ############################################################################
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

    def imageInfoChanged(self):
        if(len(self.imageAddition.lineEdit.text()) !=0 and len(self.imageAddition.lineEdit_3.text()) != 0):
            self.imageAddition.pushButton.setEnabled(True)
        else:
            self.imageAddition.pushButton.setEnabled(False)


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
        self.analysis = self.setAnalysis()

        self.central_widget.addWidget(self.home)
        self.central_widget.addWidget(self.createCase)
        self.central_widget.addWidget(self.caseManager)
        self.central_widget.addWidget(self.imageManager)
        self.central_widget.addWidget(self.imageAddition)
        self.central_widget.addWidget(self.analysis)

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

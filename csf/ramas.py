import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QUrl
import sqlite3 as lite
import time

from dbSchema import initDatabase
from views.home import Ui_HomePage
from views.createCase import Ui_CreateCase
from views.caseManager import Ui_CaseManager
from views.imageManager import Ui_ImageManager
from views.addImage import Ui_AddImage
from views.analysis import Ui_Analysis
from views.moduleManager import Ui_ModuleManager
from views.browserWidget import Browser

from models.caseModel import CaseModel
from models.imageModel import ImageModel
from models.moduleModel import ModuleModel

from analyzer import Analyzer
from moduleConfigParser import readModuleInfo
from moduleConfigParser import readRecordFields

dbName = 'ramas.db'
showAnalysisTime = False

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
        pixmap = QtGui.QPixmap("./views/logo.jpg")
        self.home.label.setPixmap(pixmap)
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

    def setModuleManager(self):
        self.moduleManager = Ui_ModuleManager()
        self.moduleManager.setupUi(self.moduleManager)
        self.moduleManager.pushButton.clicked.connect(self.addModule)
        self.moduleManager.pushButton.setEnabled(False)
        self.moduleManager.pushButton_3.setEnabled(False)
        self.moduleManager.pushButton_3.clicked.connect(self.deleteModule)
        self.moduleManager.pushButton_4.clicked.connect(self.cancelModuleManager)
        self.moduleManager.pushButton_5.clicked.connect(self.searchModule)
        self.moduleManager.lineEdit_2.setReadOnly(True)
        self.moduleManager.lineEdit_3.textChanged.connect(self.moduleInfoChanged)

        self.moduleModel = ModuleModel(self.moduleManager.listView_2, self.dbCon)
        self.moduleModel.populate()
        self.moduleManager.listView_2.setModel(self.moduleModel)
        self.moduleManager.listView_2.selectionModel().selectionChanged.connect(self.moduleSelected)
        return self.moduleManager

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
        #self.imageManager.listView.clicked.connect(self.imageSelected)
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
        return self.imageManager

    def setAddImage(self):
        self.imageAddition = Ui_AddImage()
        self.imageAddition.setupUi(self.imageAddition)
        self.imageAddition.pushButton.clicked.connect(self.addImage)
        self.imageAddition.pushButton.setEnabled(False)
        self.imageAddition.pushButton_2.clicked.connect(self.cancelImageAdding)
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
        self.central_widget.setCurrentWidget(self.moduleManager)

    ############################################################################
    # MODULE MANAGER CALLBACKS
    ############################################################################
    def searchModule(self):
        moduleLocation = QtGui.QFileDialog.getOpenFileName()
        self.moduleManager.lineEdit_3.setText(moduleLocation)

    def addModule(self):
        moduleConfig = str(self.moduleManager.lineEdit_3.text())
        if(not os.path.isfile(moduleConfig)):
            msg = "File does not exist."
            reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)
        else:
            try:
                name, description = readModuleInfo(moduleConfig)
                table_fields = readRecordFields(moduleConfig)
                self.moduleModel.insertModule(name,description,table_fields)
            except lite.Error, e:
                msg = "This module was already added to Ramas."
                reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)
        #TODO Exceptions for ill-configured config files
        self.moduleModel = ModuleModel(self.moduleManager.listView_2, self.dbCon)
        self.moduleModel.populate()
        self.moduleManager.listView_2.setModel(self.moduleModel)
        self.moduleManager.listView_2.selectionModel().selectionChanged.connect(self.moduleSelected)


    def moduleInfoChanged(self):
        if(len(self.moduleManager.lineEdit_3.text()) != 0):
            self.moduleManager.pushButton.setEnabled(True)
        else:
            self.moduleManager.pushButton.setEnabled(False)

    def moduleSelected(self):
        self.moduleManager.pushButton_3.setEnabled(True)
        moduleIndex = self.moduleManager.listView_2.selectedIndexes()
        description = self.moduleModel.fetchModuleDescription(moduleIndex[0].data().toString())
        self.moduleManager.lineEdit_2.setText(description)

    def deleteModule(self):
        moduleIndex = self.moduleManager.listView_2.selectedIndexes()
        del_msg = "Are you sure you want to delete module " + moduleIndex[0].data().toString() + "?"
        reply = QtGui.QMessageBox.warning(self, 'Message', del_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if(reply == QtGui.QMessageBox.Yes):
            self.moduleModel.deleteModule(moduleIndex[0].row(), moduleIndex[0].data().toString())
            self.moduleModel = ModuleModel(self.moduleManager.listView_2, self.dbCon)
            self.moduleModel.populate()
            self.moduleManager.listView_2.setModel(self.moduleModel)
            self.moduleManager.listView_2.selectionModel().selectionChanged.connect(self.moduleSelected)
        else:
            pass

    def cancelModuleManager(self):
        self.central_widget.setCurrentWidget(self.home)
    ############################################################################
    # NEW CASE CALLBACKS
    ############################################################################
    def addCase(self):
        #update available cases shown in list
        name = self.createCase.lineEdit.text()
        description = self.createCase.lineEdit_2.text()
        try:
            self.caseModel.insertCase(name, description)
            self.createCase.lineEdit.clear()
            self.createCase.lineEdit_2.clear()
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
        self.caseManager.pushButton.setAutoDefault(False)
        self.caseManager.pushButton.setDefault(True)
        self.caseManager.pushButton_3.setEnabled(True)
        caseIndex = self.caseManager.listView.selectedIndexes()
        if(len(caseIndex) > 0):
            description = self.caseModel.fetchCaseDescription(caseIndex[0].data().toString())
            self.caseManager.lineEdit.setText(description)

    def deleteCase(self):
        #Get row index of selected case
        caseIndex = self.caseManager.listView.selectedIndexes()
        del_msg = "Are you sure you want to delete all information pertaining to case " + caseIndex[0].data().toString() + "?"
        reply = QtGui.QMessageBox.warning(self, 'Message', del_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if(reply == QtGui.QMessageBox.Yes):
            self.caseModel.deleteCase(caseIndex[0].row(), caseIndex[0].data().toString())
            self.caseManager.lineEdit.clear()
            if(len(self.caseManager.listView.selectedIndexes()) == 0):
                self.caseManager.pushButton.setEnabled(False)
                self.caseManager.pushButton_3.setEnabled(False)
        else:
            pass

    ############################################################################
    # IMAGE MANAGER CALLBACKS
    ############################################################################

    def imageSelected(self):
        self.imageManager.pushButton_2.setEnabled(True)
        self.imageManager.pushButton_3.setEnabled(True)
        imageIndex = self.imageManager.listView.selectedIndexes()
        if(len(imageIndex) > 0):
            fileHash, description, date = self.imageModel.fetchImageInfo(imageIndex[0].data().toString(), self.current_case)
            if(not self.imageModel.verifyHash(imageIndex[0].data().toString())):
                msg = "Image has changed on disk. Please restore image file."
                reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)
                self.imageManager.lineEdit.clear()
                self.imageManager.lineEdit_2.clear()
                self.imageManager.lineEdit_3.clear()
                self.imageManager.pushButton_5.setEnabled(False)
                self.imageManager.pushButton_2.setEnabled(False)
                self.moduleModel = ModuleModel(self.imageManager.listView_2, self.dbCon)
                self.moduleModel.populate()
                self.imageManager.listView_2.setModel(self.moduleModel)

            else:
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
        imageIndex = self.imageManager.listView.selectedIndexes()
        fileHash, description, date = self.imageModel.fetchImageInfo(imageIndex[0].data().toString(), self.current_case)
        self.analysis.widget.load(QUrl('audit_result/' + fileHash + '/audit.html'))
        self.analysis.widget.show()

    def analyse(self):
        imageIndex = self.imageManager.listView.selectedIndexes()
        if(len(imageIndex) == 0):
            msg = "No image has been selected for analysis."
            reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)
        else:
            imageLocation = str(imageIndex[0].data().toString())
            fileHash, description, date = self.imageModel.fetchImageInfo(imageIndex[0].data().toString(), self.current_case)

            modulesToApply = []
            for index in range(self.moduleModel.rowCount()):
                if(self.moduleModel.item(index).isCheckable()):
                    if(self.moduleModel.item(index).checkState()):
                        modulesToApply.append(str(self.moduleModel.item(index).text()))

            if(len(modulesToApply) > 0):
                analyzer = Analyzer()
                analyzer.setup(modulesToApply, imageLocation, fileHash, self.current_case)
                if(showAnalysisTime):
                    initTime = time.time()

                analyzer.analysisLoop()

                if(showAnalysisTime):
                    endTime = time.time()
                    print "Elapsed time:"
                    print endTime - initTime

                #Refresh analysed modules and enable result view
                if(self.imageModel.wasImageAnalysed(fileHash)):
                    self.imageManager.pushButton_5.setEnabled(True)
                else:
                    self.imageManager.pushButton_5.setEnabled(False)

                self.moduleModel.populateUnprocessedModules(fileHash)
            else:
                msg = "No module has been selected for analysing the image."
                reply = QtGui.QMessageBox.warning(self, 'Message', msg, QtGui.QMessageBox.Ok)



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
        self.imageManager.pushButton_3.setEnabled(False)
        self.moduleModel.clear()
        self.moduleModel.populate()

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

    def cancelImageAdding(self):
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
        self.moduleManager = self.setModuleManager()
        self.imageManager = self.setImageManager()
        self.imageAddition = self.setAddImage()
        self.caseManager = self.setCaseManager()
        self.analysis = self.setAnalysis()

        self.central_widget.addWidget(self.home)
        self.central_widget.addWidget(self.createCase)
        self.central_widget.addWidget(self.caseManager)
        self.central_widget.addWidget(self.moduleManager)
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

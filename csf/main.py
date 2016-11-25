import sys, os
from PyQt4 import QtGui

from views.home import Ui_HomePage
from views.createCase import Ui_CreateCase
from views.caseManager import Ui_CaseManager
from views.imageManager import Ui_ImageManager

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
        self.createCase.lineEdit.textChanged.connect(self.caseNameChanged)
        self.createCase.lineEdit_2.textChanged.connect(self.caseNameChanged)
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


        item = QtGui.QStandardItem()
        item.setText('Item text')
        item2 = QtGui.QStandardItem()
        item2.setText('Item text')

        self.caseModel = QtGui.QStandardItemModel(self.caseManager.listView)
        self.caseModel.appendRow(item)
        self.caseModel.appendRow(item2)
        self.caseManager.listView.setModel(self.caseModel)
        return self.caseManager

    def setImageManager(self):
        self.imageManager = Ui_ImageManager()
        self.imageManager.setupUi(self.imageManager)
        self.imageManager.listView.clicked.connect(self.imageSelected)
        self.imageManager.pushButton.clicked.connect(self.addImage)
        self.imageManager.pushButton_3.setEnabled(False)
        self.imageManager.pushButton_3.clicked.connect(self.deleteImage)
        self.imageManager.pushButton_2.clicked.connect(self.analyse)
        self.imageManager.pushButton_4.clicked.connect(self.cancelImageManager)

        self.imageModel = QtGui.QStandardItemModel(self.imageManager.listView)
        self.imageManager.listView.setModel(self.imageModel)
        return self.imageManager

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

    def caseNameChanged(self):
        if(len(self.createCase.lineEdit.text()) !=0 and len(self.createCase.lineEdit_2.text()) != 0):
            self.createCase.pushButton.setEnabled(True)
        else:
            self.createCase.pushButton.setEnabled(False)

    def installModules(self):
        print "To be implemented"
        #self.central_widget.setCurrentWidget(self.page)

    def addCase(self):
        #update available cases shown in list
        self.central_widget.setCurrentWidget(self.caseManager)

    def addImage(self):
        #open dialog to select files
        imageLocation = QtGui.QFileDialog.getOpenFileName()
        imageName = os.path.basename(str(imageLocation))

        print "imageLocation should be kept in BD"
        item = QtGui.QStandardItem()
        item.setText(imageName)
        self.imageModel.appendRow(item)

    def analyse(self):
        #open dialog to select files
        print "analyse"

    def deleteCase(self):
        #Get row index of selected case
        caseIndex = self.caseManager.listView.selectedIndexes()
        for i in caseIndex:
            print i.data().toString()
            self.caseModel.takeRow(i.row())

        print "delete all case-related data from Database"

    def deleteImage(self):
        #Get row index of selected image
        caseIndex = self.imageManager.listView.selectedIndexes()
        #caseIndex list has only one elem
        for i in caseIndex:
            print i.data().toString()
            self.imageModel.takeRow(i.row())

        #Select image, enable delete button and remove images
        print "delete image related data from DB"

    def caseManager(self):
        self.central_widget.setCurrentWidget(self.caseManager)

    def cancelCaseManager(self):
        self.central_widget.setCurrentWidget(self.home)

    def cancelImageManager(self):
        self.central_widget.setCurrentWidget(self.caseManager)

    def manageImages(self):
        #open case relative to previous choice
        #populate imageList
        self.central_widget.setCurrentWidget(self.imageManager)


    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.home = self.setHomepage()
        self.createCase = self.setCreateCase()
        self.imageManager = self.setImageManager()
        self.caseManager = self.setCaseManager()


        self.central_widget.addWidget(self.home)
        self.central_widget.addWidget(self.createCase)
        self.central_widget.addWidget(self.caseManager)
        self.central_widget.addWidget(self.imageManager)


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

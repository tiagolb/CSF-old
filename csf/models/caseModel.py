from PyQt4 import QtGui

class CaseModel(QtGui.QStandardItemModel):

	def __init__(self, parent, dbConnection):
		super(CaseModel, self).__init__(parent)
		self.dbCon = dbConnection

	def populate(self):
		cur = self.dbCon.cursor()
		cur.execute("SELECT NAME FROM FCASE")
		rows = cur.fetchall()
		for row in rows:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def insertCase(self, name, description):
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO FCASE(NAME, DESCRIPTION) VALUES (?, ?)",
			(str(name), str(description)))
		self.dbCon.commit()

		item = QtGui.QStandardItem()
		item.setEditable(False)
		item.setText(name)

		self.appendRow(item)

	def deleteCase(self, row, name):
		#TODO Delete case-related data from the database
		cur = self.dbCon.cursor()
		cur.execute("DELETE FROM FCASE WHERE NAME=?", (str(name),))
		self.dbCon.commit()

		self.takeRow(row)

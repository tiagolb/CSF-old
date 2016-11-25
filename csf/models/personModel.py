from PyQt4 import QtGui

class PersonModel(QtGui.QStandardItemModel):

	def __init__(self, parent, dbConnection):
		super(PersonModel, self).__init__(parent)
		self.dbCon = dbConnection

	def populate(self):
		cur = self.dbCon.cursor()
		cur.execute("SELECT NAME FROM PERSON")
		rows = cur.fetchall()
		for row in rows:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def insertModule(self, name, case_name, link):
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO PERSON(NAME, CASE_NAME, LINK) VALUES (?, ?, ?)",
			(str(name), str(case_name), str(link))
		self.dbCon.commit()

		item = QtGui.QStandardItem()
		item.setEditable(False)
		item.setText(name)

		self.appendRow(item)

	def deleteModule(self, row, name, case_name):
		cur = self.dbCon.cursor()
		cur.execute("DELETE FROM PERSON WHERE NAME=? AND CASE_NAME=?", (str(name), str(case_name)))
		self.dbCon.commit()

		self.takeRow(row)

from PyQt4 import QtGui

class ModuleModel(QtGui.QStandardItemModel):

	def __init__(self, parent, dbConnection):
		super(ModuleModel, self).__init__(parent)
		self.dbCon = dbConnection

	def populate(self):
		cur = self.dbCon.cursor()
		cur.execute("SELECT NAME FROM MODULE")
		rows = cur.fetchall()
		for row in rows:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def insertModule(self, name):
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO MODULE(NAME) VALUES (?)",
			(str(name),)
		self.dbCon.commit()

		item = QtGui.QStandardItem()
		item.setEditable(False)
		item.setText(name)

		self.appendRow(item)

	def deleteModule(self, row, name):
		cur = self.dbCon.cursor()
		cur.execute("DELETE FROM MODULE WHERE NAME=?", (str(name),))
		self.dbCon.commit()

		self.takeRow(row)

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
			item.setSelectable(False)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def populateUnprocessedModules(self, imageHash):
		self.clear()

		cur = self.dbCon.cursor()
		cur.execute("SELECT NAME FROM MODULE")
		rows = cur.fetchall()
		all_modules = []
		for row in rows:
			all_modules.append(row[0])

		processed_modules = []
		for module in all_modules:
			cur.execute("SELECT MODULE FROM MESSAGE WHERE MODULE=? AND DUMP_HASH=?", (module, str(imageHash)))
			r = cur.fetchall()
			if(len(r) > 0):
				if(r[0][0] not in processed_modules):
					processed_modules.append(r[0][0])
					print "added " + r[0][0]


		for m in all_modules:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setSelectable(False)
			item.setCheckable(True)
			item.setText(m)
			if(m in processed_modules):
				item.setCheckState(True)
				item.setCheckable(False)
			self.appendRow(item)
		self.dbCon.commit()


	def insertModule(self, name):
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO MODULE(NAME) VALUES (?)",(str(name),))
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

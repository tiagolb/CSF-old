from PyQt4 import QtGui

class ModuleModel(QtGui.QStandardItemModel):

	def __init__(self, parent, dbConnection):
		super(ModuleModel, self).__init__(parent)
		self.dbCon = dbConnection

	def populate(self):
		self.clear()
		cur = self.dbCon.cursor()
		cur.execute("SELECT NAME FROM MODULE")
		rows = cur.fetchall()
		for row in rows:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setSelectable(True)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def fetchModuleDescription(self, name):
		cur = self.dbCon.cursor()
		cur.execute("SELECT DESCRIPTION FROM MODULE WHERE NAME = ?", (str(name),))
		rows = cur.fetchall()
		self.dbCon.commit()
		return rows[0][0]

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
			query = "SELECT ID FROM " + module + "_MSG WHERE DUMP_HASH=?"

			cur.execute(query, (str(imageHash),))
			r = cur.fetchall()
			if(len(r) > 0):
				if(module not in processed_modules):
					processed_modules.append(module)

		for m in processed_modules:
			print "[processed_modules] " + m


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


	def insertModule(self, name, description, table_fields):
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO MODULE(NAME, DESCRIPTION) VALUES (?, ?)",(name, description))

		query = "CREATE TABLE " + name + "_MSG(\
         ID                INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,\
         DUMP_HASH         BINARY(32)  NOT NULL,\
         CASE_NAME         TEXT        NOT NULL,"

		for field in table_fields:
			query += field + "            TEXT        NOT NULL,"

		query += "FOREIGN KEY (DUMP_HASH)       REFERENCES IMAGE(DUMP_HASH),\
         		FOREIGN KEY (CASE_NAME)       REFERENCES FCASE(NAME))"

		cur.execute(query)
		self.dbCon.commit()


	def deleteModule(self, row, name):
		cur = self.dbCon.cursor()
		cur.execute("DELETE FROM MODULE WHERE NAME=?", (str(name),))
		query = "DROP TABLE IF EXISTS " + str(name) + "_MSG"
		cur.execute(query)
		self.dbCon.commit()

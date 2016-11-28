from PyQt4 import QtGui

class MessageModel(QtGui.QStandardItemModel):

	def __init__(self, parent, dbConnection):
		super(MessageModel, self).__init__(parent)
		self.dbCon = dbConnection

	def populate(self, case_name):
		self.clear() #clear model to prevent record repetition on navigating
		cur = self.dbCon.cursor()
		cur.execute("SELECT CONTENT FROM MESSAGE WHERE CASE_NAME=?", (str(case_name),))
		rows = cur.fetchall()
		for row in rows:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def insertMessage(self, dump_hash, case_name, module, sender, receiver, content, timestamp):
		dump_hash = self.md5Hash(location)
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO MESSAGE (DUMP_HASH, CASE_NAME, MODULE, SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP) VALUES (?, ?, ?, ?, ?, ?, ?)",
			(dump_hash, str(case_name), str(module), str(sender), str(receiver), str(content), timestamp))
		self.dbCon.commit()

		item = QtGui.QStandardItem()
		item.setEditable(False)
		item.setText(location)

		self.appendRow(item)

	def deleteMessage(self, row, message_id):
		#TODO Delete image-related data from the database
		cur = self.dbCon.cursor()
		cur.execute("DELETE FROM MESSAGE WHERE ID=?", (message_id,))
		self.dbCon.commit()

		self.takeRow(row)


	def fetchMessageInfo(self, message_id):
		cur = self.dbCon.cursor()
		cur.execute("SELECT SENDER, RECEIVER, CONTENT, MESSAGE_TIMESTAMP FROM MESSAGE WHERE ID = ?", (message_id,))
		rows = cur.fetchall()
		self.dbCon.commit()
		return rows[0][0], rows[0][1], rows[0][2]

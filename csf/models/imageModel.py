from PyQt4 import QtGui
import hashlib

class ImageModel(QtGui.QStandardItemModel):

	def __init__(self, parent, dbConnection):
		super(ImageModel, self).__init__(parent)
		self.dbCon = dbConnection

	def md5Hash(self,file_location):
	    hash_md5 = hashlib.md5()
	    with open(file_location, "rb") as f:
	        for chunk in iter(lambda: f.read(4096), b""):
	            hash_md5.update(chunk)
	    return hash_md5.hexdigest()

	def populate(self, case_name):
		self.clear() #clear model to prevent record repetition on navigating
		cur = self.dbCon.cursor()
		cur.execute("SELECT DUMP_LOCATION FROM IMAGE WHERE CASE_NAME=?", (str(case_name),))
		rows = cur.fetchall()
		for row in rows:
			item = QtGui.QStandardItem()
			item.setEditable(False)
			item.setText(row[0])
			self.appendRow(item)
		self.dbCon.commit()

	def insertImage(self, location, case_name, description, date):
		dump_hash = self.md5Hash(location)
		cur = self.dbCon.cursor()
		cur.execute("INSERT INTO IMAGE(DUMP_HASH, CASE_NAME, DESCRIPTION, AQUISITION_DATE, DUMP_LOCATION) VALUES (?, ?, ?, ?, ?)",
			(dump_hash, str(case_name), str(description), date, str(location)))
		self.dbCon.commit()

		item = QtGui.QStandardItem()
		item.setEditable(False)
		item.setText(location)

		self.appendRow(item)

	def deleteImage(self, row, location, case_name):
		#TODO Delete image-related data from the database
		cur = self.dbCon.cursor()
		cur.execute("DELETE FROM IMAGE WHERE DUMP_LOCATION=? AND CASE_NAME=?", (str(location), str(case_name)))
		self.dbCon.commit()

		self.takeRow(row)


	def fetchImageInfo(self, location, case_name):
		cur = self.dbCon.cursor()
		cur.execute("SELECT DUMP_HASH, DESCRIPTION, AQUISITION_DATE FROM IMAGE WHERE DUMP_LOCATION = ? AND CASE_NAME = ?", (str(location),str(case_name)))
		rows = cur.fetchall()
		self.dbCon.commit()
		return rows[0][0], rows[0][1], rows[0][2]

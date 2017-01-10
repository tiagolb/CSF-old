from PyQt4 import QtGui
import hashlib
import shutil
import os

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
		cur = self.dbCon.cursor()
		imgHash = self.md5Hash(location)

		cur.execute("DELETE FROM IMAGE WHERE DUMP_LOCATION=? AND CASE_NAME=?", (str(location), str(case_name)))

		cur.execute("DELETE FROM GLOBAL_MSG WHERE DUMP_HASH=? AND CASE_NAME=?", (str(imgHash), str(case_name)))

		#Erase messages pertaining to the image/Case
		cur.execute("SELECT NAME FROM MODULE")
		rows = cur.fetchall()


		for r in rows:
			query = "DELETE FROM " + str(r[0]) + "_MSG WHERE DUMP_HASH=? AND CASE_NAME=?"
			cur.execute(query, (str(imgHash), str(case_name)))

		#If is it the last version of the image in use among several cases, delete audit html
		cur.execute("SELECT DUMP_HASH FROM IMAGE WHERE DUMP_LOCATION=?", (str(location),))
		rows = cur.fetchall()
		if(len(rows) == 0):
			if(os.path.exists('./audit_result/'+ imgHash)):
				shutil.rmtree('./audit_result/'+ imgHash)

		self.dbCon.commit()
		self.takeRow(row)


	def fetchImageInfo(self, location, case_name):
		cur = self.dbCon.cursor()
		cur.execute("SELECT DUMP_HASH, DESCRIPTION, AQUISITION_DATE FROM IMAGE WHERE DUMP_LOCATION = ? AND CASE_NAME = ?", (str(location),str(case_name)))
		rows = cur.fetchall()
		self.dbCon.commit()

		return rows[0][0], rows[0][1], rows[0][2]


	def verifyHash(self, location):
		cur = self.dbCon.cursor()
		currentHash = self.md5Hash(str(location))

		cur.execute("SELECT DUMP_HASH FROM IMAGE WHERE DUMP_LOCATION = ?", (str(location),))
		rows = cur.fetchall()
		self.dbCon.commit()

		return currentHash == rows[0][0]

	def wasImageAnalysed(self, imageHash):
		cur = self.dbCon.cursor()
		cur.execute("SELECT NAME FROM MODULE")
		rows = cur.fetchall()
		all_modules = []
		for row in rows:
			all_modules.append(row[0])

		for module in all_modules:
			cur.execute("SELECT * FROM " + module + "_MSG WHERE DUMP_HASH=?", (str(imageHash),))
			rows = cur.fetchall()
		 	if(len(rows) > 0):
				return True
			else:
				continue
		return False

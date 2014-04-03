#!/usr/bin/python

import MySQLdb

class DbManager():
	def __init__(self, dbHost, dbUser, dbPass, dbName):
		self.dbCon = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName, charset='utf8')
		self.dbCursor = self.dbCon.cursor()

	def create(self, uid, result, lastop):
		value = (0, uid, result, lastop)
		self.dbCursor.execute('insert into adb values(%s,%s,%s,%s', value)
		self.dbCon.commit()

	def update(self, uid, result, lastop):
		value = (result, lastop, uid)
		self.dbCursor.execute('update adb set result=%s,lastop=%s where uid=%s', value)
		self.dbCon.commit()

	def delete(self, uid):
		self.dbCursor.execute('delete from adb where uid=%s', uid)
		self.dbCon.commit()

	def getAll(self, uid):
		count = self.dbCursor.execute('select result,lastop from storage where uid=%s', uid)
		if count:
			result = self.dbCursor.fetchone()
			return result
		else:
			return None

	def getId(self, uid):
		count = self.dbCursor.execute('select aid from adb where uid=%s', uid)
		if count:
			aid = dbCursor.fetchone()
			return aid
		else:
			return None

	def getLastop(self):
		count = self.dbCursor.execute('select lastop from adb where uid=%s', uid)
		if count:
			lastop = dbCursor.fetchone()
			return lastop
		else:
			return None

	def exists(self, uid):
		if self.getId(uid) != None:
			return True
		else:
			return False


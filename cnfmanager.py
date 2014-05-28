#!/usr/bin/python

import ConfigParser
import os

class CnfManager():
	def load(self, cnfFile):
		if not os.path.isfile(cnfFile):
			cnfFile = './nda.cnf'

		cf = ConfigParser.ConfigParser()
		cf.read(cnfFile)

		self.cnfData = {}
		self.cnfData['dbHost'] = cf.get('db', 'dbHost')
		self.cnfData['dbUser'] = cf.get('db', 'dbUser')
		self.cnfData['dbPass'] = cf.get('db', 'dbPass')
		self.cnfData['dbName'] = cf.get('db', 'dbName')
		self.cnfData['comPort'] = int(cf.get('com', 'comPort'))

	def get_cnf_data(self):
		return self.cnfData

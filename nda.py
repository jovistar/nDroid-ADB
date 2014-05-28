#!/usr/bin/python

from cnfmanager import CnfManager
from dbmanager import DbManager
from ndlcom import NdlCom
from netmanager import NetManager
import ndutil

from twisted.internet import reactor

def nda_loop():
	ndutil.setTimezone()

	ndlCom = NdlCom('nDroid-ADB', '127.0.0.1', 12322)
	ndlCom.doCom('Initiating')

	ndlCom.doCom('Loading Config')
	cnfManager = CnfManager()
	cnfManager.load('./nda.cnf')
	cnfData = cnfManager.get_cnf_data()

	ndlCom.doCom('Connecting to DB')
	dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])

	netManager = NetManager()
	netManager.setNdlCom(ndlCom)
	netManager.setDbManager(dbManager)

	reactor.listenUDP(cnfData['comPort'], netManager)
	ndlCom.doCom('Listening Com Port')
	reactor.run()

if __name__ == '__main__':
	nda_loop()

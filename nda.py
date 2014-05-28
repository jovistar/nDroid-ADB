#!/usr/bin/python

from cnfmanager import CnfManager
from dbmanager import DbManager
from ndlcom import NdlCom
from netmanager import NetManager
import ndutil
import sys
import getopt

from twisted.internet import reactor

def nda_loop(doInit):
    ndutil.setTimezone()

    ndlCom = NdlCom('nDroid-ADB', '127.0.0.1', 12322)
    ndlCom.doCom('Initiating')

    ndlCom.doCom('Loading Config')
    cnfManager = CnfManager()
    cnfManager.load('./nda.cnf')
    cnfData = cnfManager.get_cnf_data()

    ndlCom.doCom('Connecting to DB')
    dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])

    if doInit:
        dbManager.create_table()

    netManager = NetManager()
    netManager.setNdlCom(ndlCom)
    netManager.setDbManager(dbManager)

    reactor.listenUDP(cnfData['comPort'], netManager)
    ndlCom.doCom('Listening Com Port')
    reactor.run()

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'i')

    doInit = False

    for opt, arg in opts:
        if opt in ('-i'):
            doInit = True

    nda_loop(True)

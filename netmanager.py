#!/usr/bin/python

from twisted.internet.protocol import DatagramProtocol
from ndlcom import NdlCom
from dbmanager import DbManager
from msgmanager import MsgManager
import ndutil

class NetManager(DatagramProtocol):
    def setNdlCom(self, ndlCom):
        self.ndlCom = ndlCom
        self.msgManager = MsgManager()

    def setDbManager(self, dbManager):
        self.dbManager = dbManager

    def datagramReceived(self, data, (host, port)):
        retCode, result = self.msgManager.resRequest(data)
        if retCode != 0:
            self.ndlCom.doCom('Bad Request FROM %s:%s' % (host, port))
        else:
            responseData = None
            self.ndlCom.doCom('Request: %s From %s:%s' % (result['request'], host, port))
            if result['request'] == 'create_item':
                responseData = self.dispatch_create_item(result['uid'], result['state'])
            elif result['request'] == 'delete_item':
                responseData = self.dispatch_delete_item(result['uid'])
            elif result['request'] == 'update_state':
                responseData = self.dispatch_update_state(result['uid'], result['state'])
            elif result['request'] == 'get_item':
                responseData = self.dispatch.get_item(result['uid'])
            elif result['request'] == 'get_state':
                responseData = self.dispatch.get_state(result['uid'])
            elif result['request'] == 'get_last_update':
                responseData = self.dispatch_get_last_update(result['uid'])

            msg = self.msgManager.genResponse(responseData)
            self.transport.write(msg, (host, port))

     def dispatch_create_item(self, uid, state):
        responseData = {}
        if state not in ['b', 'm', 'u']:
            responseData['response'] = 1
            return responseData
        
        if self.dbManager.exists(uid):
            responseData = self.dispatch_update_item(uid, state)
        else:
            self.dbManager.create_item(uid, state, ndutil.getCreated())
            responseData['response'] = 0
        return responseData
        
     def dispatch_delete_item(self, uid):
        responseData = {}
        if self.dbManager.exists(uid):
            self.dbManager.delete_item(uid)
            responseData['response'] = 0
        else:
            responseData['response'] = 1
        return responseData

     def dispatch_update_state(self, uid, state):
        responseData = {}
        
        if state not in ['b', 'm', 'u']:
            responseData['response'] = 1
            return responseData

        if self.dbManager.exists(uid):
            self.dbManager.update_state(uid, state, ndutil.getCreated())
            responseData['response'] = 0
        else:
            responseData = self.dispatch_create_item(uid, state)
        return responseData

     def dispatch_get_item(self, uid):
        responseData = {}
        result = self.dbManager.get_item(uid)
        if result == None:
            responseData['response'] = 1
        else:
            responseData['response'] = 0
            responseData['item'] = result
        return responseData

     def dispatch_get_state(self, uid):
        responseData = {}
        result = self.dbManager.get_state(uid)
        if result == None:
            responseData['response'] = 1
        else:
            responseData['response'] = 0
            responseData['state'] = result
        return responseData
      
     def dispatch_get_last_update(self, uid):
        responseData = {}
        result = self.dbManager.get_last_update(uid)
        if result == None:
            responseData['response'] = 1
        else:
            responseData['response'] = 0
            responseData['last_update'] = result
        return responseData

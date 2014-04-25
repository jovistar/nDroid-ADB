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
		self.ndlCom.doCom('Request from %s:%d' % (host, port))
		self.dispatch(data, host, port)

	def dispatch(self, data, host, port):
		retCode, result = self.msgManager.resRequest(data)
		if retCode != 0:
			self.ndlCom.doCom('ERROR')
		else:
			responseData = {}
			if result['request'] == 'create':
				self.ndlCom.doCom('Request: CREATE')
				if self.dbManager.exists(result['uid']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0
					self.dbManager.create(result['uid'], result['result'], ndutil.getCreated())

			if result['request'] == 'delete':
				self.ndlCom.doCom('Request: DELETE')
				if not self.dbManager.exists(result['uid']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0
					self.dbManager.delete(result['uid'])

			if result['request'] == 'get':
				self.ndlCom.doCom('Request: GET')
				if not self.dbManager.exists(result['uid']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0
					responseData['result'], resposneData['lastop'] = self.dbManager.getAll(result['uid'])

			if result['request'] == 'update':
				self.ndlCom.doCom('Request: UPDATE')
				if not self.dbManager.exists(result['uid']):
					responseData['response'] = 1
				else:
					responseData['response'] = 0
					self.dbManager.update(uid, result['result'], ndutil.getCreated())

			msg = self.msgManager.genResponse(responseData)
			self.transport.write(msg, (host, port))

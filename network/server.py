# -*- coding: utf-8 -*-
import socket
import time
import warnings

class server:
	peers = ["192.168.43.1"]	

	def __init__(self, port = 2020):

		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conn = None		

		print("Server IP = 192.168.43.1")
		self.sock.bind(('192.168.43.1', port))		

	def listen(self):		

		if self.conn == None:
			self.sock.listen(1)
			self.conn, addr = self.sock.accept()
			print('Got connection from', addr)			

			self.peers.append(addr[0]) if addr[0] not in self.peers else self.peers		
			print('Peers = ', self.peers)			

		return self.recvData()	

	def sendData(self, data):		

		try:
			self.conn.send(data.encode('utf-8'))
		except:
			warnings.warn("Socket Not Available")		

	def recvData(self):
		
		data=[]
		#print('in recvData')		

		try:
			tempData = self.conn.recv(1024).decode('utf-8')
		except:
			self.conn = None
			warnings.warn("Socket Not Available")

			return ''		

		if tempData == '':
			return ''

		test = tempData.split('$', 2)
		dataLen = int(test[1])
		tempData= test[2]
		recvLen = 0
		#print("DataLen=", dataLen)		

		while recvLen < dataLen:



			#print("Data Rx\n", tempData)

			recvLen += len(tempData)

			data.append(tempData)

			

			if ( dataLen - recvLen) < 1024:

				msgLen = dataLen - recvLen
				
				if msgLen == 0:
					break


			else:
				msgLen = 1024

			

			#print(recvLen)

			#print(msgLen)

			try:

				tempData = self.conn.recv(msgLen)
				tempData = tempData.decode('utf-8')
			except:

				warnings.warn("Socket Not Available")				



		#print(data)

		data = ''.join(data)

		#print(data)

		return data

		

	def close(self):

		self.sock.close()

		self.conn = None

# -*- coding: utf-8 -*-

import socket
# import time
import warnings

class client:
    
    def __init__(self, ip = "192.168.43.1", port = 2020):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
        try:
            self.sock.connect((ip, port))
        except:
            print("Server Not Available")     

        
    # def sendKeyBundle(self, filename = "publicKeyBundle.pub"):
        
    #     file = open(filename,'r')
        
    #     keyData = file.read(1024)
        
    #     #self.sock.send(b"Registration Request")
        
    #     while keyData:
    #         #print("Sending Data")
    #         self.sock.send(keyData.encode('utf-8'))
    #         print("Data Sent")
            
    #         keyData = file.read(1024)
            
    #     file.close()
            
    def sendData(self, data):
        try:
            #print(data)
            dataLen = len(data)
            # print(dataLen)
            numBlocks = int(dataLen/1024)
            # print(numBlocks)
            
            if numBlocks > 0:
                for i in range(numBlocks):
                    tempData = data[i*1024:(i+1)*1024].encode('utf-8')
                    #print(tempData)
                    self.sock.send(tempData)
            else:
                i=0
                
            tempData = data[numBlocks*1024:].encode('utf-8')
            #print(tempData)
            self.sock.send(tempData)
        except:
            warnings.warn("Socket Not Available")
        
    def recvData(self):
                
        data=[]
        
        try:
            tempData = self.sock.recv(1024).decode('utf-8')
            print(tempData)
            test = tempData.split('$')
            dataLen = int(test[1])
            tempData= test[2].encode('utf-8')
        except:
            warnings.warn("Socket Not Available")
            return
            
       
        recvLen = 0
        #print("DataLen=", dataLen)
        
        while recvLen < dataLen:
        	#print("Data Rx\n", tempData)
        	recvLen += len(tempData)
        	data.append(tempData.decode('utf-8'))
        	if ( dataLen - recvLen) < 1024:
        		msgLen = dataLen - recvLen
        	else:
        		msgLen = 1024
        		
        	try:
        		tempData = self.sock.recv(msgLen).decode('utf-8')
        	except:
        		warnings.warn("Socket Not Available")
        		
        #print(data)
        data = ''.join(data)
        #print(data)
        return data
        
    def close(self):
        self.sock.close()
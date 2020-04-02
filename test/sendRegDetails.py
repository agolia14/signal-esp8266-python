# -*- coding: utf-8 -*-

from network.client import client
from util.message import Message as msg
from helper.registration import ClientRegistration

cl = client()

regClient = ClientRegistration()
regId, req = regClient.reqRegistrationId()
cl.sendData(req)

resp = cl.recvData()
respType, respRegId = msg.retrieveMessage(resp)

if respType == msg.REG_ID:
    
    if respRegId != regId:
        cl.close()
    else:
        req = regClient.registerKeyBundle()
        cl.sendData(req)
        
cl.close()

#print(keyInfo)
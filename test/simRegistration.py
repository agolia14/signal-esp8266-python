# -*- coding: utf-8 -*-
from helper.registration import ClientRegistration, ServerRegistration
from util.message import Message as msg

def remove_length(data):
    return data.split('$', 2)[2]

sharedData = ""

regClient = ClientRegistration()
regIdClient, req = regClient.reqRegistrationId()
sharedData = remove_length(req)

reqType, reqData = msg.retrieveMessage(sharedData)

regServer = ServerRegistration()
	
if reqType == msg.REG_ID:    
	regIdServer = reqData
	sharedData = remove_length(regServer.respRegistrationId(regIdServer))

respType, respRegId = msg.retrieveMessage(sharedData)

if respType == msg.REG_ID:
    
    if respRegId != regIdClient:
        exit
    else:
        req = regClient.registerKeyBundle()
        sharedData = remove_length(req)

reqType, reqData = msg.retrieveMessage(sharedData)
    
if reqType == msg.KEY_BUNDLE:
	regServer.saveKeyBundle(reqData)
# -*- coding: utf-8 -*-
import sys
sys.path.append('/storage/emulated/0/Python/client_server')

from network.server import server
from util.message import message as msg
from helper.registration import ServerRegistration

try:
    ser = server()
    
    while True:
        req = ser.listen()
        
        if req == '':
            continue
            
        reqType, reqData = msg.retrieveMessage(req)
        regServer = ServerRegistration()
    
        if reqType == msg.REG_ID:
            regId = reqData            
            resp = regServer.respRegistrationId(regId)
            ser.sendData(resp)
                
        elif reqType == msg.KEY_BUNDLE:
            keyBundle=reqData
            
            if(regServer.saveKeyBundle(reqData)):
                print('Done')
            else:
                print("RegId Mismatch")
        else:
            print(reqType)
            
except:
    #import sys
    sys.exit()
    print(sys.exc_info())

ser.close()
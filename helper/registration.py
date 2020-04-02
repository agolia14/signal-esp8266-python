# -*- coding: utf-8 -*-
from util.message import Message as msg
from util.keystore import KeyStore

 
class ClientRegistration:
        
    def __init__(self):
        
        self.ks = KeyStore()
        self.ks.generateKeysPairs()
    
        self.publicKeyBundle = self.ks.createPublicKeyBundle()
        self.privateKeyBundle = self.ks.createPrivateKeyBundle()
        self.regId = self.privateKeyBundle[self.ks.REG_ID]
        
        self.ks.saveSelfKeyBundle(self.ks.PUBLIC_KEY)
        self.ks.saveSelfKeyBundle(self.ks.PRIVATE_KEY)
    
    def reqRegistrationId(self):
        return self.regId, msg.prepareRegistrationRequest(self.regId)
    
    def registerKeyBundle(self):
        keyBundle = self.ks.preProcessKeyBundle(self.publicKeyBundle.copy(), self.ks.WRITE_FILE)
#        print(keyBundle)
        return msg.preparePublicKeyBundle(keyBundle)
    
class ServerRegistration:
    
    def __init__(self):
        self.ks = KeyStore()
    
    def respRegistrationId(self, regId):
        
        self.regId = regId
        
        if self.ks.isRegistrationIdExist(regId):
            return msg.prepareRegistrationRequest("")
        else:
            return msg.prepareRegistrationRequest(regId)
        
    def saveKeyBundle(self, keyBundle):
        
        if keyBundle[self.ks.REG_ID] == self.regId:
            self.ks.saveKeyBundle(self.regId, keyBundle, False)
            return True
        else:
            return False
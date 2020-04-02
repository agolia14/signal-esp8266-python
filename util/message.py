# -*- coding: utf-8 -*-

class Message:
# =============================================================================
#     Initialize Message Class
# =============================================================================
    __MSG_REGISTRATION = 0x24
    __MSG_KEY_BUNDLE = 0x01
    __MSG_Message = 0x93
    
    REG_ID = "regId"
    KEY_BUNDLE = "keyBundle"
    Message = "Message"
    
    __msgType = {__MSG_REGISTRATION: REG_ID,
               __MSG_KEY_BUNDLE: KEY_BUNDLE,
               __MSG_Message: Message}
    
    def __init__(self, registrationId=None, preKeyId=None,
                 signedPreKeyId=None, publicBaseKey=None, identityKey=None):   
        
        self.registrationId = registrationId
        self.preKeyId = preKeyId
        self.signedPreKeyId = signedPreKeyId
        self.publicBaseKey = publicBaseKey
        self.identityKey = identityKey        
     
# =============================================================================
#     Convert Message in form of dictionary to string
#     Patch length with the msg
#     
#     req => Request in form of dictionary
#     msg => msg ready to be transmitted
# =============================================================================
    @staticmethod
    def requestMessage(req):
        msg = repr(req)
        msg = '$' + repr(len(msg)) + '$' + msg
        
        return msg
# =============================================================================
#     Send Registration Request to Server
#     regId -> Registration ID, if not provided will be provided by server randomly
# =============================================================================
    @staticmethod
    def prepareRegistrationRequest(regId = None):     
        req = {'type': Message.__MSG_REGISTRATION,
               'data': regId}
        
        return Message.requestMessage(req)
    
    @staticmethod
    def preparePublicKeyBundle(keyBundle):
        req = {'type': Message.__MSG_KEY_BUNDLE,
               'data': keyBundle}
        
        return Message.requestMessage(req)
    
    def prepareMessage(self, msg):
        req = {'type': self.__MSG_Message,               
               'data': msg}
        
        
        return Message.requestMessage(req)
        
    @staticmethod
    def retrieveMessage(msg):
        
        req = eval(msg)            
        reqType = Message.__msgType[req["type"]]        
        data = req['data']
        
        return reqType, data
    
    @staticmethod
    def processRegistration(msg):
        
        pass
    
    @staticmethod
    def processPublicKeyBundle(msg):
        pass
    
    @staticmethod
    def processMessage(msg):
        pass
# -*- coding: utf-8 -*-
from nacl.public import PrivateKey
import json

class KeyPair:
    
    def __init__(self, publicKey = None, privateKey = None):
        self.privateKey = privateKey
        self.publicKey = publicKey
        
    def generate(self):
        self.privateKey = PrivateKey.generate()
        self.publicKey = self.privateKey.public_key
        
        return self
        
    def getPublicKey(self):
        return self.publicKey
    
    def getPrivateKey(self):
        return self.privateKey
    
class PreKeyRecord:
    
    def __init__(self, _id, keyPair):

        self.id = _id
        self.keyPair = keyPair

    def getId(self):
        return self.id

    def getKeyPair(self):
        return self.keyPair
    
class SignedPreKeyRecord:
    def __init__(self, _id=None, timestamp=None, keyPair=None, signature=None, serialized=None):

        self.id = _id
        self.keyPair = keyPair
        self.signature = signature
        self.timestamp = timestamp

    def getId(self):
        return self.id

    def getTimestamp(self):
        return self.timestamp

    def getKeyPair(self):
        return self.keyPair

    def getSignature(self):
        return self.signature
        
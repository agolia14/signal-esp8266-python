# -*- coding: utf-8 -*-

from x3dh.keyGen import KeyGen
import os.path

# =============================================================================
#   Generates, Stores and loads key from memory
# =============================================================================
class KeyStore:

    PUBLIC_KEY = 0x01
    PRIVATE_KEY = 0x02

    IDENTITY_KEY = 'identityKey'
    PRE_KEY = 'preKey'
    SIGNED_PRE_KEY = 'signedPreKey'
    REG_ID = "regId"

    READ_FILE = 0x01
    WRITE_FILE = 0x02

    def __init__(self):
        pass

# =============================================================================
#   Generate Keys for the communication establishment between devices
#   Need to be done only once at the time of installation
# =============================================================================
    def generateKeysPairs(self):

        startId = 1
        
        if self.isPrivateKeyExist():
            pass
        else:
            self.identityKeyPair = KeyGen.generateIdentityKeyPair()
            self.registrationId  = KeyGen.generateRegistrationId()
            self.preKeysPair = KeyGen.generatePreKeys(startId, 100)
            self.signedPreKeyPair = KeyGen.generateSignedPreKey(self.identityKeyPair, 5)

# =============================================================================
#    Save all the public keys in a single dictionary
#    It is further processed so that it can be shared to send public keys
#    to other users
# =============================================================================
    def createPublicKeyBundle(self):

        identityKey = self.identityKeyPair.getPublicKey()
        preKeyLen = len(self.preKeysPair)
        preKey = dict()

        for _id in range(preKeyLen):
            preKeyId = self.preKeysPair[_id].getId()
            preKeyPublicKey = self.preKeysPair[_id].getKeyPair().getPublicKey()

            preKey[preKeyId] = preKeyPublicKey

        signedPreKey = self.signedPreKeyPair.getKeyPair().getPublicKey()

        keyBundle = dict()
        keyBundle[self.IDENTITY_KEY] = identityKey
        keyBundle[self.PRE_KEY] = preKey
        keyBundle[self.SIGNED_PRE_KEY] = signedPreKey
        keyBundle[self.REG_ID] = self.registrationId
        
        self.publicKeyBundle = keyBundle.copy()

        return keyBundle

# =============================================================================
#    Save all the private keys in a single dictionary
#    Makes encryption and signing process easier
# =============================================================================
    def createPrivateKeyBundle(self):

        identityKey = self.identityKeyPair.getPrivateKey()
        preKeyLen = len(self.preKeysPair)
        preKey = dict()

        for _id in range(preKeyLen):

            preKeyId = self.preKeysPair[_id].getId()
            preKeyPublicKey = self.preKeysPair[_id].getKeyPair().getPrivateKey()
            preKey[preKeyId] = preKeyPublicKey

        signedPreKey = self.signedPreKeyPair.getKeyPair().getPrivateKey()

        keyArray = dict()
        keyArray[self.IDENTITY_KEY] = identityKey
        keyArray[self.PRE_KEY] = preKey
        keyArray[self.SIGNED_PRE_KEY] = signedPreKey
        keyArray[self.REG_ID] = self.registrationId
        
        self.privateKeyBundle = keyArray.copy()

        return keyArray

# =============================================================================
#    Preprocess the Key Bundle:
#        1. Before Saving it to File
#        2. After Reading it from file
#       
#    keyBundle => Dictionary in which keys are stored as strings
#    direc => Preprocessing for read/write request (READ_FILE, WRITE_FILE)
#    keyType => Selction for private and public key while reading file
#   
#    Returns => dictionary having key values
# =============================================================================
    def preProcessKeyBundle(self, keyBundle, direc, keyType = None):

        if direc == self.WRITE_FILE:            
            keyBundle[self.IDENTITY_KEY] = keyBundle[self.IDENTITY_KEY].__bytes__()
            keyBundle[self.SIGNED_PRE_KEY] = keyBundle[self.SIGNED_PRE_KEY].__bytes__()
            preKey = keyBundle[self.PRE_KEY]

            keyBundle[self.PRE_KEY] = {key: preKey[key].__bytes__() for key in preKey}

        elif direc == self.READ_FILE:
            keyBundle = eval(''.join(keyBundle))

            if keyType == self.PRIVATE_KEY:
                keyBundle[self.IDENTITY_KEY] = KeyGen.toSigningKey( keyBundle[self.IDENTITY_KEY] )
                keyBundle[self.SIGNED_PRE_KEY] = KeyGen.toPrivateKey( keyBundle[self.SIGNED_PRE_KEY] )
                preKey = keyBundle[self.PRE_KEY]

                keyBundle[self.PRE_KEY] = {key: KeyGen.toPrivateKey( preKey[key] ) for key in preKey}

            elif keyType == self.PUBLIC_KEY:
                keyBundle[self.IDENTITY_KEY] = KeyGen.toVerifyKey( keyBundle[self.IDENTITY_KEY] )
                keyBundle[self.SIGNED_PRE_KEY] = KeyGen.toPublicKey( keyBundle[self.SIGNED_PRE_KEY] )
                preKey = keyBundle[self.PRE_KEY]

                keyBundle[self.PRE_KEY] = {key: KeyGen.toPublicKey( preKey[key] ) for key in preKey}

            else:
                raise ValueError("Wrong Key Type")

        else:
            raise ValueError("Wrong preprocessing direction")

        return keyBundle

    def saveSelfKeyBundle(self, keyType):

        if keyType == self.PUBLIC_KEY:
            filename = "PublicKeyBundle"
            keyBundle = self.publicKeyBundle.copy()
        elif keyType == self.PRIVATE_KEY:
            filename = "PrivateKeyBundle"
            keyBundle = self.privateKeyBundle.copy()
        else:
            raise ValueError("keyType not correct")

        return self.saveKeyBundle(filename, keyBundle)

    def loadSelfKeyBundle(self, keyType):

        if keyType == self.PUBLIC_KEY:
            filename = "PublicKeyBundle"
        elif keyType == self.PRIVATE_KEY:
            filename = "PrivateKeyBundle"
        else:
            raise ValueError("keyType not correct")

        return self.loadKeyBundle(filename, keyType)

    def saveKeyBundle(self, filename, keyBundle, preProcess = True):
        filename = "../data/" + filename  + ".pub"
        print(filename)

        if preProcess == True:
            keyBundle = self.preProcessKeyBundle(keyBundle, self.WRITE_FILE)
        
        keyBundle = repr(keyBundle)
        file = open(filename,'w')
        file.write(keyBundle)
        file.close()

    def loadKeyBundle(self, filename, keyType = PUBLIC_KEY):

        if( (keyType != self.PUBLIC_KEY ) and (keyType != self.PRIVATE_KEY) ):
            raise ValueError("Wrong Keytype")

        filename = "../data/" + filename  + ".pub"

        if not(os.path.exists(filename)):
            raise FileNotFoundError

        file = open(filename,'r')
        keys = file.readlines()
        keyBundle = self.preProcessKeyBundle(keys, self.READ_FILE, keyType)
        file.close()

        return keyBundle

    def isRegistrationIdExist(self, regId):

        filename = "../data/" + regId + ".pub"

        if os.path.exists(filename):
            return True
        else:
            return False
        
    def isPrivateKeyExist(self):

        filename = "../data/PrivateKeyBundle.pub"

        if os.path.exists(filename):
            return True
        else:
            return False

    def bytesToKeys(keyBundle):
        pass
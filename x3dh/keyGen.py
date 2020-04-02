# -*- coding: utf-8 -*-
import nacl.encoding
import nacl.signing
from nacl.public import Box, PrivateKey, PublicKey
import uuid

from x3dh.keyStructs import KeyPair, PreKeyRecord, SignedPreKeyRecord

import time
import math, os, binascii

class KeyGen:
    
    maxPreKeys = 0xFFFFFF
    
    def __init__(self, maxPreKeys = 0xFFFFFF):
        KeyGen.maxPreKeys = maxPreKeys

    @staticmethod
    def generateIdentityKeyPair():
        """
        Generate an identity key pair.  Clients should only do this once,
        at install time.`
        @return the generated IdentityKeyPair.
        """
        signKey = nacl.signing.SigningKey.generate()
        verifyKey = signKey.verify_key

        return KeyPair(verifyKey, signKey)

    @staticmethod
    def generateRegistrationId():
        """
        Generate a registration ID.  Clients should only do this once,
        at install time.
        """
        regId = uuid.getnode()
        return hex(regId).replace('0x', '')

    @staticmethod
    def getRandomSequence(max=4294967296):
        size = int(math.log(max) / math.log(2)) / 8
        rand = os.urandom(int(size))
        randh = binascii.hexlify(rand)
        return int(randh, 16)

    @staticmethod
    def generatePreKeys(start, count):
        """
        Generate a list of PreKeys.  Clients should do this at install time, and
        subsequently any time the list of PreKeys stored on the server runs low.

        PreKey IDs are shorts, so they will eventually be repeated.  Clients should
        store PreKeys in a circular buffer, so that they are repeated as infrequently
        as possible.

        @param start The starting PreKey ID, inclusive.
        @param count The number of PreKeys to generate.
        @return the list of generated PreKeyRecords.
        """
        results = []
        start -= 1
        keyPair = KeyPair()
        
        for i in range(0, count):
            
            preKeyId = ((start + i) % (KeyGen.maxPreKeys - 1)) + 1
            
            results.append( PreKeyRecord( preKeyId, keyPair.generate() ) )

        return results

    @staticmethod
    def generateSignedPreKey(identityKeyPair, signedPreKeyId):
        
        keyPair = KeyPair().generate()
        
        signature = identityKeyPair.getPrivateKey().sign( keyPair.getPublicKey().__bytes__() )

        spk = SignedPreKeyRecord(signedPreKeyId, int(round(time.time() * 1000)), keyPair, signature)

        return spk

    @staticmethod
    def generateSharedKey(privateKey, publicKey):
        box = Box(privateKey, publicKey)
        
        return box.shared_key()
    
    @staticmethod
    def generateSenderSigningKey():
        return KeyPair.generate()

    @staticmethod
    def generateSenderKey():
        return os.urandom(32)

    @staticmethod
    def generateSenderKeyId():
        return KeyGen.getRandomSequence(2147483647)
    
    @staticmethod
    def toSigningKey(key):
        return nacl.signing.SigningKey(key)
    
    @staticmethod
    def toPrivateKey(key):
        return PrivateKey(key)
    
    @staticmethod
    def toVerifyKey(key):
        return nacl.signing.VerifyKey(key)
    
    @staticmethod
    def toPublicKey(key):
        return PublicKey(key)
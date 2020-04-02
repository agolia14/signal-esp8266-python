from x3dh.keyGen import KeyGen
from network.client import client
from util.keystore import keystore
import json
startId = 1

keyStore = keystore()
keyStore.generateKeysBundle()
pubKeys = keyStore.preProcessKeyBundle( keyStore.createPublicKeyBundle(), keyStore.WRITE_FILE )

file = open('pubKey.txt', 'w')
file.write(str(pubKeys))
file.close()

file = open('pubKey.txt', 'r')
print(keyStore.preProcessKeyBundle(file.readlines(), keyStore.READ_FILE, keyStore.PUBLIC_KEY))
#Store identityKeyPair somewhere durable and safe.
#Store registrationId somewhere durable and safe.

#Store preKeys in PreKeyStore.
#Store signed prekey in SignedPreKeyStore.
'''
sessionStore      = MySessionStore()
preKeyStore       = MyPreKeyStore()
signedPreKeyStore = MySignedPreKeyStore()
identityStore     = MyIdentityKeyStore()

# Instantiate a SessionBuilder for a remote recipientId + deviceId tuple.
sessionBuilder = SessionBuilder(sessionStore, preKeyStore, signedPreKeyStore,
                                                   identityStore, recipientId, deviceId)

# Build a session with a PreKey retrieved from the server.
sessionBuilder.process(retrievedPreKey)

sessionCipher = SessionCipher(sessionStore, recipientId, deviceId)
message       = sessionCipher.encrypt("Hello world!")

deliver(message.serialize())
'''

#cl = client()
#publicKeyBundle = KeyBundle(identityKeyPair, preKeys, signedPreKey)
#keyInfo = publicKeyBundle.createPublicKeyBundle()
#cl.sendKeyBundle()
#print(cl.recv())
#cl.close()

#print(keyInfo)
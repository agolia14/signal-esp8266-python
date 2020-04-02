from util.keystore import KeyStore

remoteId = 'b86daa75f886'
ks = KeyStore()

localKeybundle = ks.loadSelfKeyBundle(ks.PRIVATE_KEY)
remoteKeyBundle = ks.loadKeyBundle(remoteId)
print(remoteKeyBundle[ks.IDENTITY_KEY])
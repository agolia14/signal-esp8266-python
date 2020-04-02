from util.keystore import KeyStore as ks

class SessionStore:
    
    IDENTITY_KEY = ks.IDENTITY_KEY
    PRE_KEY = ks.PRE_KEY
    SIGNED_PRE_KEY = ks.SIGNED_PRE_KEY    
    
    def __init__(self, localKeyBundle, remoteKeyBundle):
        self.localKeyBundle = localKeyBundle
        self.remoteKeyBundle = remoteKeyBundle
        
    def getSenderBaseKey():
        
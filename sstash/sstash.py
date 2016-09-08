from .crypto_stash import CryptoStash
from .inner_stash import InnerStash
from .exceptions import SSError, SSCryptoError

class SecureStash:
    def __init__(self,path,password,debug=False):
        if not debug:
            # Production:
            self._crypto_stash = CryptoStash(path,password)
        else:
            # Less iterations for faster tests:
            self._crypto_stash = \
                    CryptoStash(path,password,default_num_iterations=100)

    def read_value(self,key):
        """
        Read a value from secure stash corresponding to key.
        """
        store = self._crypto_stash.read_store()
        istash = InnerStash(store)
        return istash.read_value(key)

    def get_children(self,key):
        """
        Get children of a key.
        """
        store = self._crypto_stash.read_store()
        istash = InnerStash(store)
        return istash.get_children(key)

    def write_value(self,key,value):
        """
        Write value to key.
        """
        store = self._crypto_stash.read_store()
        istash = InnerStash(store)
        istash.write_value(key,value)
        self._crypto_stash.write_store(istash.get_store())


    def remove_key(self,key):
        """
        Remove a key from the secure stash.
        """
        store = self._crypto_stash.read_store()
        istash = InnerStash(store)
        value = istash.remove_key(key)
        self._crypto_stash.write_store(istash.get_store())
        return value



import json
from hashlib import pbkdf2_hmac


class SecureStash:
    def __init__(self,path,password):
        self._password = password
        self._path = path

    def read_value(self,key):
        """
        Read a value from secure stash corresponding to key.
        """
        pass

    def write_value(self,key,value):
        """
        Write value to key.
        """
        pass


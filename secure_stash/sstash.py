import json
from hashlib import pbkdf2_hmac
from jsonschema import validate
import nacl.secret
from .schema import OUTER_SCHEMA
from .exceptions import SSError, SSCryptoError
from encode_utils import hex_str_to_bytes, bytes_to_hex_str


class SecureStash:
    def __init__(self,path,password):
        self._password = password.encode('utf-8')
        self._path = path

    def get_store(self):
        with open(self._path,'r',encoding='ascii') as fr:
            outer_data = json.load(fr)

        try:
            validate(outer_data,OUTER_SCHEMA)
        except ValidationError:
            raise SSError("Invalid outer schema")

        # Derive key from password:
        dk = pbkdf2_hmac(outer_data['hash'],
                self._password,
                outer_data['salt'],
                outer_data['iterations'])

        if len(dk) < nacl.secret.SecretBox.KEY_SIZE:
            raise SSCryptoError("Derived key is not long enough")

        enc_bytes = hex_str_to_bytes(outer_data["enc_blob"])

        box = nacl.secret.SecretBox(key)
        inner_data = box.decrypt(enc_bytes)
        return json.load(inner_data.decode('utf-8'))


    def commit_store(self,store):
        assert False


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

    def remove_key(self,key):
        """
        Remove a key from the secure stash.
        """
        pass


import os
import json
from hashlib import pbkdf2_hmac
from jsonschema import validate
import nacl.secret
from .schema import OUTER_SCHEMA
from .exceptions import SSError, SSCryptoError
from encode_utils import hex_str_to_bytes, bytes_to_hex_str

# Default parameters for pbkdf2:
HASH = 'sha512'
SALT_LEN = 32
NUM_ITERATIONS = 2**18


class CryptoStash:
    def __init__(self,path,password):
        self._password = password.encode('utf-8')
        self._path = path

        if not os.path.isfile(self._path):
            self._initialize_stash()

        self._load_dkey()


    def _load_dkey(self):
        """
        Load derived key from existing stash file.
        """
        with open(self._path,'r',encoding='ascii') as fr:
            outer_data = json.load(fr)

        try:
            validate(outer_data,OUTER_SCHEMA)
        except ValidationError:
            raise SSError("Invalid outer schema")

        self._hash = outer_data['hash']
        self._salt = outer_data['salt']
        self._iterations = outer_data['iterations']

        # Derive key from password:
        dk = pbkdf2_hmac(outer_data['hash'],
                self._password,
                outer_data['salt'],
                outer_data['iterations'],
                nacl.secret.SecretBox.KEY_SIZE)

        self._box = nacl.secret.SecretBox(dk)


    def _initialize_stash(self):
        """
        Create an empty stash at self._path with password self._password
        """
        outer_data = {
            'hash': HASH,
            'salt': os.urandom(SALT_LEN),
            'iterations': NUM_ITERATIONS,
        }

        # Derive key from password:
        dk = pbkdf2_hmac(outer_data['hash'],
                self._password,
                outer_data['salt'],
                outer_data['iterations'],
                nacl.secret.SecretBox.KEY_SIZE
                )

        if len(dk) < nacl.secret.SecretBox.KEY_SIZE:
            raise SSCryptoError("Derived key is not long enough")

        empty_store = json.dump({}).encode('utf-8')
        outer_data['enc_blob'] = bytes_to_hex_str(
                self._box.encrypt(empty_store))

        with open(self._path,'w',encoding='ascii') as fw:
            json.dump(outer_data,fw)



    def read_store(self):
        """
        Get the store from file.
        """
        with open(self._path,'r',encoding='ascii') as fr:
            outer_data = json.load(fr)

        try:
            validate(outer_data,OUTER_SCHEMA)
        except ValidationError:
            raise SSError("Invalid outer schema")

        enc_bytes = hex_str_to_bytes(outer_data["enc_blob"])
        inner_data = self._box.decrypt(enc_bytes)
        return json.loads(inner_data.decode('utf-8'))


    def write_store(self,store):
        """
        Commit store to file.
        """
        inner_data = json.dumps(store).encode('utf-8')
        enc_bytes = self._box.encrypt(inner_data)
        enc_blob = bytes_to_hex_str(enc_bytes)

        outer_data = {
            'hash': self._hash,
            'salt': self._salt,
            'iterations': self._iterations,
            'enc_blob': enc_blob,
        }

        with open(self._path,'w',encoding='ascii') as fw:
            json.dump(outer_data,fw)


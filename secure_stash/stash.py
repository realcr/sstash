import json
from hashlib import pbkdf2_hmac
from jsonschema import validate

class SecureStashError(Exception): pass

OUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "hash": {"type": "string"},
        "salt": {"type": "string"},
        "iterations": {"type": "integer", "minimum":0},
        "enc_blob": {"type": "string"},
    },
    "required": ["hash","salt","iterations","enc_blob"],
    "additionalProperties": False,
}

INNER_SCHEMA = {
    "definitions": {
        "children": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "entry": {
                        "type": "object",
                        "properties": {
                            "children": {"$ref": "#/definitions/children"},
                            "value": {"type": "string"},
                        },
                        "required": ["children"],
                        "additionalProperties": False,
                    }
                }
            },
            "additionalProperties": False,
        },
    },
    "$ref": "#/definitions/children",
}


"""
Example json file:

hash_name: "sha256",
salt: "af1234fcadb",
iterations: 100000,
enc_blob: "345908abcdf4395840398acd",


Inside the encrypted blob:

children: {
    hello: {
        children: {
            hi: {
                children: {
                    bye: {
                        value: "bye's value",
                        children: {},
                    }
                },
            },
            some_key: {
                value: "some_key's value",
                children: {},
            }
        }
    }
}
"""

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


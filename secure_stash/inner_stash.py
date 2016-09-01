from jsonschema import validate
from jsonschema.exceptions import ValidationError
import codecs
from .schema import INNER_SCHEMA
from .exceptions import SSError,SSKeyError,SSValueError

class InnerStash:
    def __init__(self,store):
        try:
            validate(store,INNER_SCHEMA)
        except ValidationError:
            raise SSError("Invalid inner store.")

        self._store = store

    def read_value(self,key):
        """
        Read a value from the Stash
        """
        cur_node = None
        cur_children = self._store

        for i,k in enumerate(key):
            try:
                cur_node = cur_children[k]
            except KeyError:
                raise SSKeyError("Key {} was not found in store."\
                        .format(key[:i+1]))
            cur_children = cur_node["children"]

        if cur_node is None:
            raise SSKeyError("Empty key was provided: {}".format(key))

        try:
            # Return value:
            return codecs.decode(cur_node["value"].encode('ascii'),'hex')
        except KeyError:
            raise SSKeyError("Key {} was not set a value in store."\
                    .format(key[:i+1]))


    def write_value(self,key,value):
        """
        Write a value to the stash
        """
        if not isinstance(value,bytes):
            raise SSValueError("value must be of type bytes")

        cur_node = None
        cur_children = self._store

        for k in key:
            if k not in cur_children:
                cur_children[k] = {
                    "children": {},
                }

            cur_node = cur_children[k]
            cur_children = cur_node["children"]

        # Set new value:
        cur_node["value"] = codecs.encode(value,'hex').decode('ascii')

        # Just to be sure:
        try:
            validate(self._store,INNER_SCHEMA)
        except ValidationError:
            raise SSError("Store got corrupted after writing value.")

    def remove_key(self,key):
        assert False


    def get_store(self):
        return self._store

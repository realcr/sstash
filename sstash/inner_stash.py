import copy

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .schema import INNER_SCHEMA
from .exceptions import SSError,SSKeyError,SSValueError
from .encode_utils import bytes_to_hex_str, hex_str_to_bytes



class InnerStash:
    def __init__(self,store):
        self._store = copy.deepcopy(store)
        self._validate_store()

    def _validate_store(self):
        """
        Make sure that inner store matches against INNER_SCHEMA
        """
        try:
            validate(self._store,INNER_SCHEMA)
        except ValidationError:
            raise SSError("Invalid inner store.")


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
            return hex_str_to_bytes(cur_node["value"])
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
        cur_node["value"] = bytes_to_hex_str(value)

        self._validate_store()


    def remove_key(self,key):
        """
        Remove key from stash. Returns the value of this key.
        """
        cur_node = None
        cur_children = self._store

        if len(key) == 0:
            # TODO: Empty key should remove everything:
            raise SSKeyError("Empty key was provided.")

        for i,k in enumerate(key[:-1]):
            try:
                cur_node = cur_children[k]
            except KeyError:
                raise SSKeyError("Key {} was not found in store."\
                        .format(key[:i+1]))
            cur_children = cur_node["children"]


        lastk = key[-1]
        if lastk not in cur_children:
            raise SSKeyError("Key {} was not found in store."\
                    .format(key))

        last_node = cur_children[lastk]

        # Remove node:
        del cur_children[lastk]

        # Return the value of the removed node, or None is no value was found:
        if "value" not in last_node:
            return None

        self._validate_store()

        return hex_str_to_bytes(last_node["value"])


    def get_children(self,key):
        """
        Get a list of children for a key.
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

        return list(cur_children.keys())


    def get_store(self):
        return self._store

import os
from os.path import join
from .crypto_stash import CryptoStash
from .inner_stash import InnerStash
from .exceptions import SSError, SSCryptoError, SSKeyError

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

    def write_file(self,key,src_path):
        """
        Write a file into the key.
        """
        with open(src_path,'rb') as fr:
            self.write_value(key,fr.read())

    def read_file(self,key,dest_path):
        """
        Read a file from key.
        """
        with open(dest_path,'wb') as fw:
            fw.write(self.read_value(key))


    def write_dir(self,key,src_dir):
        """
        Write a directory into the key (recursively)
        """
        def inner_write_dir(prefix):
            work_path = join(src_dir,*prefix)
            for entry in os.listdir(work_path):
                fullpath = join(work_path,entry)
                if os.path.isfile(fullpath):
                    self.write_file(key + prefix + [entry],fullpath)
                else:
                    inner_write_dir(prefix + [entry])
        inner_write_dir([])


    def read_dir(self,key,dest_dir):
        """
        Read a directory from a key (recursively)
        """
        if os.path.exists(dest_dir):
            raise SSError('Path {} already exists'.format(dest_dir))

        def inner_read_dir(prefix):
            os.makedirs(join(dest_dir,*prefix))
            for child in self.get_children(key + prefix):
                fullkey = key + prefix + [child]
                has_value = True
                try:
                    self.read_value(fullkey)
                except SSKeyError:
                    has_value = False

                if has_value:
                    self.read_file(fullkey,\
                            join(dest_dir,*(prefix + [child])))
                else:
                    inner_read_dir(prefix + [child])
        inner_read_dir([])


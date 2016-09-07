Python Secure Stash
-------------------

A simple on-disk secure stash for secrets, written in python.


Basic Usage
-----------

    ```python
    >>> from secure_stash.sstash import SecureStash

    >>> ss = SecureStash('my_stash','my_password1234')

    >>> ss.write_value(['project','SomeService','token1'],b'622324c09486bf30ed3a9213954a35c34de84535')

    >>> ss.read_value(['project','SomeService','token1'])
    b'622324c09486bf30ed3a9213954a35c34de84535'

    >>> ss.write_value(['project','SomeService','token2'],b'2435e188b48f4d1778279f1ae764fa5c1d272a03')

    >>> ss.read_value(['project','SomeService','token2'])
    b'2435e188b48f4d1778279f1ae764fa5c1d272a03'

    >>> ss.remove_key(['project','SomeService','token1'])
    b'622324c09486bf30ed3a9213954a35c34de84535'

    >>> ss.read_value(['project','SomeService','token1'])
    Traceback (most recent call last):
      File "/home/real/projects/secure_stash/secure_stash/inner_stash.py", line 36, in read_value
        cur_node = cur_children[k]
    KeyError: 'token1'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/real/projects/secure_stash/secure_stash/sstash.py", line 15, in read_value
        return istash.read_value(key)
      File "/home/real/projects/secure_stash/secure_stash/inner_stash.py", line 39, in read_value
        .format(key[:i+1]))
    secure_stash.exceptions.SSKeyError: Key ['project', 'SomeService', 'token1'] was not found in store.
    ```

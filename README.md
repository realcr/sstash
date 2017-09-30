# Python Secure Stash

A simple on-disk secure stash for secrets, written in Python.
Requires Python >= 3 to work.

**This is a new project. Use with caution.**

# Basic API Usage

```python
>>> from sstash.sstash import SecureStash

>>> ss = SecureStash('my_stash', 'my_password1234')

>>> ss.write_value(['project', 'SomeService', 'token1'], b'622324c09486bf30ed3a9213954a35c34de84535')

>>> ss.read_value(['project', 'SomeService', 'token1'])
b'622324c09486bf30ed3a9213954a35c34de84535'

>>> ss.write_value(['project', 'SomeService', 'token2'], b'2435e188b48f4d1778279f1ae764fa5c1d272a03')

>>> ss.read_value(['project', 'SomeService', 'token2'])
b'2435e188b48f4d1778279f1ae764fa5c1d272a03'

>>> ss.remove_key(['project', 'SomeService', 'token1'])
b'622324c09486bf30ed3a9213954a35c34de84535'

>>> ss.read_value(['project', 'SomeService', 'token1'])
...
sstash.exceptions.SSKeyError: Key ['project', 'SomeService', 'token1'] was not found in store.

```

# Installation

First make sure you have those packages:

```
$ sudo apt install libffi-dev python3-dev
```

Then install from [PyPI](https://pypi.python.org/pypi/sstash):

```
$ pip3 install sstash
```

# Tutorial

sstash allows you to encrypt your secrets on disk using a simple Python
API. A secure stash is a single file on disk. 

To keep the data inside the data store hidden from other people, we
encrypt it using a password. 

To create a new stash file, we run a Python line of this form:

```
ss = SecureStash('my_stash','my_password1234')
```

If `my_stash` has never existed before, this line will create a new stash file
called `my_stash`. It will be empty, and it will be encrypted using the
password 'my_password1234'. If the stash `my_stash` already exists, it will
be opened.

The secure stash is built as a tree based data store.

For example, If you store the bytes `b'hello'` in the key `['a','b','c']`,
and the bytes `b'bye'` in the key `['a','b','d']`, you will get the
following tree inside the data store:

```
ss.write_value(['a', 'b', 'c'], b'hello')
ss.write_value(['a', 'b', 'd'], b'bye')

'a'
 |--'b'
     |--'c' : b'hello'
     |--'d' : b'bye'
```

If you then store the bytes `b'chocolate'` inside the key `['a','e']`, you
will get the following tree:

```
ss.write_value(['a', 'e'], b'chocolate')

'a'
 |--'b'
 |   |--'c' : b'hello'
 |   |--'d' : b'bye'
 |
 |--'e': b'chocolate'
```

If we then remove the key ``['a','b','c']`` we will get the following tree:

```
ss.remove_key(['a', 'b', 'c'])

'a'
 |--'b'
 |   |--'d' : b'bye'
 |
 |--'e': b'chocolate'
```

# Cryptography used

sstash is based on well known cryptography primitives. For key derivation
(Creating a key from the given user password) it uses pbkdf2 (Python's standard
implementation).
The random for the salt for the password is taken from `os.urandom`.

PyNaCl's Secret Key Encryption is used for encrypting the data store. PyNaCl
uses Secret Key Encryption uses Salsa20 steam cipher for encryption and
Poly1305 MAC for authentication.

All of the cryptography code can be found inside the file [`crypto_stash.py`](https://raw.githubusercontent.com/realcr/sstash/master/sstash/crypto_stash.py).

# Tests

Proudly tested by `py.test`.
To run the tests (Make sure that you are at the root directory first):

```
py.test sstash 
```

## Exceptions:

All the exceptions can be imported from

```
sstash.exceptions
```

The base exception is `sstash.exceptions.SSError`.

Other exceptions are:

- sstash.exceptions.SSKeyError
- sstash.exceptions.SSValueError
- sstash.exceptions.SSCryptoError


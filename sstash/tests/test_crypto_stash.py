import pytest
from ..crypto_stash import CryptoStash
from ..exceptions import SSCryptoError, SSError


def test_init_nonexistent(tmp_file_path):
    """
    Test the initialization of a CryptoStash (When stash file doesn't exist)
    """
    cs = CryptoStash(tmp_file_path,'my_password',default_num_iterations=1000)

def test_basic_operation(tmp_file_path):
    """
    Test the initialization of a CryptoStash (When stash file doesn't exist)
    """
    # Initialization:
    cs = CryptoStash(tmp_file_path,'my_password',default_num_iterations=1000)

    # Open again:
    cs = CryptoStash(tmp_file_path,'my_password',default_num_iterations=1000)

    my_store = {'1':2, '3':4}
    cs.write_store({1:2,3:4})
    my_store2 = cs.read_store()
    assert my_store2 == my_store


def test_wrong_password(tmp_file_path):
    """
    Test the initialization of a CryptoStash (When stash file doesn't exist)
    """
    # Initialization:
    cs = CryptoStash(tmp_file_path,'my_password',default_num_iterations=1000)

    my_store = {'1':2, '3':4}
    cs.write_store({1:2,3:4})

    # Try to load Crypto Stash with the wrong password:
    with pytest.raises(SSCryptoError):
        cs = CryptoStash(tmp_file_path,'my_password2',
                default_num_iterations=1000)


    # Try to load Crypto Stash with the correct password.
    # Should work correctly:
    cs = CryptoStash(tmp_file_path,'my_password',default_num_iterations=1000)
    cs.read_store()


def test_invalid_stash_file(tmp_file_path):
    """
    Try to read from an invalid stash file.
    """
    with open(tmp_file_path,'w',encoding='ascii') as fw:
        fw.write('I am not a stash file!')

    with pytest.raises(SSError):
        ss = CryptoStash(tmp_file_path,"my_password")

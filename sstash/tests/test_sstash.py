import os
import pytest
from ..sstash import SecureStash
from ..exceptions import SSError, SSKeyError, SSCryptoError

def test_initialization(tmp_file_path):
    ss = SecureStash(tmp_file_path,"my_password",debug=True)

def test_initialization_and_reuse(tmp_file_path):
    ss = SecureStash(tmp_file_path,"my_password",debug=True)
    ss = SecureStash(tmp_file_path,"my_password",debug=True)

def test_wrong_password(tmp_file_path):
    ss = SecureStash(tmp_file_path,"my_password",debug=True)
    with pytest.raises(SSCryptoError):
        ss = SecureStash(tmp_file_path,"my_password2",debug=True)

def test_basic_usage(tmp_file_path):
    ss = SecureStash(tmp_file_path,"my_password",debug=True)
    ss.write_value(['a','b','c'],b'abc')
    ss.write_value(['a','b'],b'ab')
    ss.write_value(['a','b','d'],b'abd')

    assert sorted(ss.get_children(['a','b'])) == sorted(['c','d'])
    assert ss.get_children(['a','b','d']) == []
    assert ss.get_children(['a','b','d']) == []

    assert ss.read_value(['a','b','c']) == b'abc'
    assert ss.read_value(['a','b']) == b'ab'
    assert ss.read_value(['a','b','d']) == b'abd'

    assert ss.remove_key(['a','b','d']) == b'abd'
    assert ss.get_children(['a','b']) == ['c']

    with pytest.raises(SSKeyError): 
        ss.read_value(['a','b','d'])

    assert ss.read_value(['a','b','c']) == b'abc'

    assert ss.read_value(['a','b','c']) == b'abc'
    assert ss.read_value(['a','b']) == b'ab'

    ss = SecureStash(tmp_file_path,"my_password",debug=True)

    assert ss.read_value(['a','b','c']) == b'abc'
    assert ss.read_value(['a','b']) == b'ab'


def test_invalid_stash_file(tmp_file_path):
    """
    Try to read from an invalid stash file.
    """
    with open(tmp_file_path,'w',encoding='ascii') as fw:
        fw.write('I am not a stash file!')

    with pytest.raises(SSError):
        ss = SecureStash(tmp_file_path,"my_password",debug=True)


def test_read_write_file(tmp_dir_path):
    """
    Test basic operation of writing/reading files to/from the stash.
    """
    stash_path = os.path.join(tmp_dir_path,'my_stash')
    file_path = os.path.join(tmp_dir_path,'my_file')
    other_file_path = os.path.join(tmp_dir_path,'my_other_file')
    file_content = b'Some bytes inside the file'

    with open(file_path,'wb') as fw:
        fw.write(file_content)

    ss = SecureStash(stash_path,"my_password",debug=True)
    ss.write_file(['a','b'],file_path)

    assert ss.read_value(['a','b']) == file_content

    ss.read_file(['a','b'],other_file_path)

    with open(other_file_path,'rb') as fr:
        assert fr.read() == file_content


def test_read_write_dir(tmp_dir_path):
    """
    Test basic operation of writing/reading directories to/from the stash.
    """
    stash_path = os.path.join(tmp_dir_path,'my_stash')
    dir_path = os.path.join(tmp_dir_path,'my_dir')

    ss = SecureStash(stash_path,"my_password",debug=True)
    ss.write_value(['a','b','c'],b'abc')
    ss.write_value(['a','b','d'],b'abd')

    ss.read_dir(['a'],dir_path)

    # Make sure that the directory structure is correct:
    assert os.listdir(dir_path) == ['b']
    b_path = os.path.join(dir_path,'b')
    assert sorted(os.listdir(b_path)) == sorted(['c','d'])
    c_path = os.path.join(b_path,'c')
    with open(c_path,'rb') as fr:
        assert fr.read() == b'abc'

    d_path = os.path.join(b_path,'d')
    with open(d_path,'rb') as fr:
        assert fr.read() == b'abd'

    # Now write the directory into the stash to a different key:
    ss.write_dir(['e'],dir_path)
    assert ss.read_value(['e','b','c']) == b'abc'
    assert ss.read_value(['e','b','d']) == b'abd' 


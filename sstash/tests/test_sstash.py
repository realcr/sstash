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
        ss = SecureStash(tmp_file_path,"my_password")


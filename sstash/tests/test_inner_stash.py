from secure_stash.inner_stash import InnerStash
from ..exceptions import SSError, SSKeyError, SSValueError
import pytest


def test_initialization():
    return InnerStash({})


def test_basic_value_assign():
    """
    Test setting and getting a value.
    """
    ins = InnerStash({})
    ins.write_value(['hello','world'],b'check')
    assert ins.read_value(['hello','world']) == b'check'


def test_value_read_failure_not_exists():
    """
    Test setting and getting a value.
    """
    ins = InnerStash({})

    with pytest.raises(SSKeyError):
        ins.read_value(['hello','world'])


def test_value_read_failure_empty_key():
    """
    Test setting and getting a value.
    """
    ins = InnerStash({})

    with pytest.raises(SSKeyError):
        ins.read_value([])

def test_value_write_failure_invalid_type():
    """
    Try writing a value not of type bytes. Should raise an exception.
    """
    ins = InnerStash({})

    with pytest.raises(SSValueError):
        ins.write_value(['hello','world'],3)

    with pytest.raises(SSValueError):
        ins.write_value(['hello','world'],"A string!")

    # Try writing a dummy class instance:
    class MyClass:
        pass

    with pytest.raises(SSValueError):
        ins.write_value(['hello','world'],MyClass())


def test_values_tree_structure():
    """
    Write various values to the tree. Make sure results are as expected
    """

    ins = InnerStash({})
    ins.write_value(['a','b','c'],b'abc')
    ins.write_value(['a','b'],b'ab')
    ins.write_value(['a','b','d'],b'abd')
    ins.write_value(['a','b','d','e'],b'abde')

    assert ins.read_value(['a','b','c']) == b'abc'
    assert ins.read_value(['a','b']) == b'ab'
    assert ins.read_value(['a','b','d']) == b'abd'
    assert ins.read_value(['a','b','d','e']) == b'abde'

    # The key ['a'] was not assigned a value:
    with pytest.raises(SSKeyError):
        ins.read_value(['a'])

def test_basic_get_store():
    """
    Make sure that get_store doesn't crash
    """

    ins = InnerStash({})
    ins.write_value(['a','b','c'],b'abc')
    ins.write_value(['a','b'],b'ab')
    ins.write_value(['a','b','d'],b'abd')
    ins.write_value(['a','b','d','e'],b'abde')

    return ins.get_store()


def test_remove_key():
    """
    Test the operation of key removal from store.
    """
    ins = InnerStash({})
    ins.write_value(['a','b','c'],b'abc')
    assert ins.remove_key(['a','b']) == None

    with pytest.raises(SSKeyError):
        ins.read_value(['a','b','c'])

    ins.write_value(['a','b','c'],b'abc')
    ins.write_value(['a','b'],b'ab')
    assert ins.remove_key(['a','b']) == b'ab'

    with pytest.raises(SSKeyError):
        ins.read_value(['a','b','c'])

    ins.write_value(['a','b','c'],b'abc')
    ins.write_value(['a','b'],b'ab')
    assert ins.remove_key(['a','b','c']) == b'abc'
    assert ins.read_value(['a','b']) == b'ab'


def test_remove_nonexistent_key():
    ins = InnerStash({})
    ins.write_value(['a','b','c'],b'abc')
    with pytest.raises(SSKeyError):
        ins.remove_key(['d','e','f'])


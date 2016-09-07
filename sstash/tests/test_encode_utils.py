from ..encode_utils import bytes_to_hex_str, hex_str_to_bytes

def test_bytes_str_conversion():
    """
    Test the validity of conversion between bytes and hex string.
    """
    some_bytes = b'some bytes.'
    some_str = bytes_to_hex_str(some_bytes)
    some_bytes2 = hex_str_to_bytes(some_str)
    some_str2 = bytes_to_hex_str(some_bytes2)
    assert some_bytes == some_bytes2
    assert some_str == some_str2
    assert isinstance(some_bytes2,bytes)
    assert isinstance(some_str2,str)

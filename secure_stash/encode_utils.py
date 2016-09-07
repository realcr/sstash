import codecs

def bytes_to_hex_str(arg_bytes):
    return codecs.encode(arg_bytes,'hex').decode('ascii')

def hex_str_to_bytes(arg_str):
    return codecs.decode(arg_str.encode('ascii'),'hex')

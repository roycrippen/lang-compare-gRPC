def xor_cipher(in_str, key):
    key_len = len(key)
    ks = bytearray(key, encoding='utf-8')
    xs = bytearray()
    for i, c in enumerate(bytearray(in_str, encoding='utf-8')):
        xs.append(c ^ ks[i % key_len])
    return xs.decode()

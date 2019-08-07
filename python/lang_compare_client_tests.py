import logging

import grpc

import lang_compare_pb2
import lang_compare_pb2_grpc


# noinspection DuplicatedCode
def test_xor_cipher_python():
    port_python = 'localhost:50052'
    print("Connecting to python lang-compare server at: {}".format(port_python))
    channel_python = grpc.insecure_channel(port_python)
    stub_python = lang_compare_pb2_grpc.LangCompareStub(channel_python)

    key = "my key"
    num = 1_000
    print("calling python xor_cipher {} times".format(num * 2))
    decrypted = ""
    for i in range(num):
        in_str = "message{0:05d}".format(i)
        response_python = stub_python.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=in_str,))
        response_cpp = stub_python.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=response_python.out_str))
        decrypted = response_cpp.out_str
        assert (decrypted == in_str)

    print("last decrypted string: '{}'\n".format(decrypted))


# noinspection DuplicatedCode
def test_xor_cipher_cpp():
    port_python = 'localhost:50051'
    print("Connecting to cpp lang-compare server at: {}".format(port_python))
    channel_python = grpc.insecure_channel(port_python)
    stub_python = lang_compare_pb2_grpc.LangCompareStub(channel_python)

    key = "my key"
    num = 1_000
    print("calling cpp xor_cipher {} times".format(num * 2))
    decrypted = ""
    for i in range(num):
        in_str = "message{0:05d}".format(i)
        response_python = stub_python.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=in_str))
        response_cpp = stub_python.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=response_python.out_str))
        decrypted = response_cpp.out_str
        assert (decrypted == in_str)

    print("last decrypted string: '{}'\n".format(decrypted))


if __name__ == '__main__':
    logging.basicConfig()
    test_xor_cipher_python()
    # test_xor_cipher_cpp()

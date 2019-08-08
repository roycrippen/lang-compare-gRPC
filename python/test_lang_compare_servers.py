import grpc

import lang_compare_pb2
import lang_compare_pb2_grpc


def test_xor_cipher(lang, port):
    port_str = 'localhost:{}'.format(port)
    print("Connecting to {} lang-compare server at: {}".format(lang, port_str))
    channel = grpc.insecure_channel(port_str)
    stub = lang_compare_pb2_grpc.LangCompareStub(channel)

    key = "my key"
    num = 1_000
    print("calling {} xor_cipher {} times".format(lang, num * 2))
    decrypted = ""
    for i in range(num):
        in_str = "message{0:05d}".format(i)
        response = stub.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=in_str))
        response = stub.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str))
        decrypted = response.out_str
        assert (decrypted == in_str)

    print("last decrypted string: '{}'\n".format(decrypted))


if __name__ == '__main__':
    test_xor_cipher('cpp', 50051)
    test_xor_cipher('python', 50052)

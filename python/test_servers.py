import unittest
import lang_compare_pb2
from lib import xor_cipher, connect_server

from hypothesis import given, settings
from hypothesis.strategies import text, characters


class CConnect:
    port = -1
    stub = None


def call_xor_cipher_twice(stub, key, s):
    # first call
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=s)
    response = stub.XorCipher(request)
    # second call with result from first
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str)
    response = stub.XorCipher(request)
    return response.out_str


class TestEncoding(unittest.TestCase):
    # random generators
    utf8_chars = text(characters(min_codepoint=0, max_codepoint=127))
    at_least_one_utf8_char = text(characters(min_codepoint=0, max_codepoint=127), min_size=1)

    # servers
    py_server = CConnect()
    cpp_server = CConnect()

    @classmethod
    def setUpClass(cls):
        unittest.TextTestRunner(verbosity=2)
        cls.py_server.port = 50052
        cls.py_server.stub = connect_server(cls.py_server.port)

        cls.cpp_server.port = 50051
        cls.cpp_server.stub = connect_server(cls.cpp_server.port)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_python_xor_cipher(self, key, s):
        self.assertEqual(xor_cipher(key, xor_cipher(key, s)), s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_python_server(self, key, s):
        result = call_xor_cipher_twice(self.py_server.stub, key, s)
        self.assertEqual(result, s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_cpp_server(self, key, s):
        result = call_xor_cipher_twice(self.cpp_server.stub, key, s)
        self.assertEqual(result, s)


if __name__ == '__main__':
    unittest.main()

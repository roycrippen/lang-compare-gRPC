import unittest
import lang_compare_pb2
from lib import xor_cipher, connect_server

from hypothesis import given, settings, Verbosity
from hypothesis.strategies import text, characters

# random generators
utf8_chars = text(characters(min_codepoint=0, max_codepoint=127))
at_least_one_utf8_char = text(characters(min_codepoint=0, max_codepoint=127), min_size=1)


class TestEncoding(unittest.TestCase):
    def setUpModule(self):
        unittest.TextTestRunner(verbosity=2)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_python_xor_cipher(self, key, s):
        self.assertEqual(xor_cipher(key, xor_cipher(key, s)), s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_python_server(self, key, s):
        channel, stub = connect_server(50052)
        response = stub.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=s))
        response = stub.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str))
        self.assertEqual(response.out_str, s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_cpp_server(self, key, s):
        channel, stub = connect_server(50051)
        response = stub.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=s))
        response = stub.XorCipher(lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str))
        self.assertEqual(response.out_str, s)


if __name__ == '__main__':
    # test_python_xor_cipher()
    # test_python_server()
    # test_cpp_server()
    unittest.main()

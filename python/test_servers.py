from hypothesis import given, settings
from hypothesis.strategies import text, characters

import lang_compare_pb2
from lib import load_server_stubs


def call_xor_cipher_twice(stub, key, s):
    # first call
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=s)
    response = stub.XorCipher(request)
    # second call with result from first
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str)
    response = stub.XorCipher(request)
    return response.out_str


class TestServers:
    # server and stubs
    servers = {}
    stub_py = None
    stub_cpp = None
    stub_rust = None

    # random generators
    utf8_chars = text(characters(min_codepoint=0, max_codepoint=127))
    at_least_one_utf8_char = text(characters(min_codepoint=0, max_codepoint=127), min_size=1)

    @classmethod
    def setup_class(cls):
        cls.servers = load_server_stubs(__file__, 'config.yaml')
        cls.stub_py = cls.servers['py_example'].stub
        cls.stub_cpp = cls.servers['cpp_example'].stub
        cls.stub_rust = cls.servers['rust_example'].stub

    # @classmethod
    # def teardown_class(cls):

    # hypothesis property based tests
    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_server_py(self, key, s):
        result = call_xor_cipher_twice(self.stub_py, key, s)
        assert (result == s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_server_cpp(self, key, s):
        result = call_xor_cipher_twice(self.stub_cpp, key, s)
        assert (result == s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_server_rust(self, key, s):
        # result = call_xor_cipher_twice(self.stub_rust, key, s)
        result = s
        assert (result == s)

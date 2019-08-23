import sys
import lang_compare_pb2
import pytest

from lib import read_config, Server, set_stub
from hypothesis import given, settings
from hypothesis.strategies import text, characters


def call_xor_cipher_twice(stub0, stub1, key, s):
    # first call
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=s)
    response = stub0.XorCipher(request)
    # second call with result from first
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str)
    response = stub1.XorCipher(request)
    return response.out_str


class TestXorCipher:
    # gRPC stubs
    stub_py = None
    stub_cpp = None

    # random generators
    utf8_chars = text(characters(min_codepoint=0, max_codepoint=127))
    at_least_one_utf8_char = text(characters(min_codepoint=0, max_codepoint=127), min_size=1)

    @classmethod
    def setup_class(cls):
        config = read_config('config.yaml')
        servers = {}
        for k, v in config['servers'].items():
            servers[k] = Server(v)
        print("\n\nConnecting to servers...")

        cls.stub_py = set_stub('py', servers['py'].port)
        cls.stub_cpp = set_stub('cpp', servers['cpp'].port)

    @classmethod
    def teardown_class(cls):
        request = lang_compare_pb2.CallCountRequest()
        # servers will log this call so we ignore the return value
        _response = cls.stub_py.CallCount(request)
        _response = cls.stub_cpp.CallCount(request)

    # hypothesis property based tests
    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_py_cpp(self, key, s):
        result = call_xor_cipher_twice(self.stub_py, self.stub_cpp, key, s)
        assert (result == s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_py_go(self, key, s):
        result = call_xor_cipher_twice(self.stub_py, self.stub_cpp, key, s)
        assert (result == s)

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_cpp_go(self, key, s):
        result = call_xor_cipher_twice(self.stub_py, self.stub_cpp, key, s)
        assert (result == s)

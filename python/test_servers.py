import subprocess
import time
import unittest
import lang_compare_pb2
from lib import connect_server, read_config, Server

from hypothesis import given, settings
from hypothesis.strategies import text, characters


def call_xor_cipher_twice(stub, key, s):
    # first call
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=s)
    response = stub.XorCipher(request)
    # second call with result from first
    request = lang_compare_pb2.XorCipherRequest(key=key, in_str=response.out_str)
    response = stub.XorCipher(request)
    return response.out_str


class TestWithXorCipher(unittest.TestCase):
    # random generators
    utf8_chars = text(characters(min_codepoint=0, max_codepoint=127))
    at_least_one_utf8_char = text(characters(min_codepoint=0, max_codepoint=127), min_size=1)

    # server stubs
    stubs = []
    processes = []

    @classmethod
    def setUp(cls):
        unittest.TextTestRunner(verbosity=2)
        config = read_config('config.yaml')

        for item in config['servers']:
            server = Server(list(item.values())[0])
            if server.type == 'py':
                cls.processes.append(subprocess.Popen(['python3', server.file]))
                time.sleep(1)
            elif server.type == 'cpp':
                cls.processes.append(subprocess.Popen([server.file]))
                time.sleep(0.5)
            else:
                err_str = "Invalid server type in config.yaml: {}".format(server.type)
                raise RuntimeError(err_str)
            cls.stubs.append(connect_server(server.port))

    @classmethod
    def tearDown(cls):
        for stub in cls.stubs:
            request = lang_compare_pb2.CallCountRequest()
            # servers will log this call so we ignore the return value
            _response = stub.CallCount(request)
        for p in cls.processes:
            p.kill()

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_servers(self, key, s):
        for stub in self.stubs:
            result = call_xor_cipher_twice(stub, key, s)
            self.assertEqual(result, s)


if __name__ == '__main__':
    unittest.main()

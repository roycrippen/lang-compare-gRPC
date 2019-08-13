import subprocess
import time
import unittest
import lang_compare_pb2

from lib import connect_server, read_config, Server, Runner
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
    servers = {}
    processes = []
    langs = []

    @classmethod
    def setUp(cls):
        unittest.TextTestRunner(verbosity=2)
        config = read_config('config.yaml')

        print("\n\nConnecting to servers...")
        for item in config['servers']:
            server = Server(list(item.values())[0])
            if server.type in ['py', 'cpp']:
                cls.processes.append(subprocess.Popen(server.cmd.split(' ')))
            else:
                err_str = "Invalid server type in config.yaml: {}".format(server.type)
                raise RuntimeError(err_str)
            cls.servers[server.type] = server
            time.sleep(0.5)

        for k, v in cls.servers.items():
            v.stub = connect_server(v.port)

        for elem in config['runners']:
            k, v = list(elem.items())[0]
            if k == 'test_servers':
                cls.langs = Runner(v).langs

    @classmethod
    def tearDown(cls):
        for k, v in cls.servers.items():
            request = lang_compare_pb2.CallCountRequest()
            # servers will log this call so we ignore the return value
            _response = v.stub.CallCount(request)
        time.sleep(2)
        for p in cls.processes:
            p.kill()

    @given(key=at_least_one_utf8_char, s=utf8_chars)
    @settings(max_examples=100)
    def test_servers(self, key, s):
        for lang in self.langs:
            stub = self.servers[lang].stub
            result = call_xor_cipher_twice(stub, key, s)
            self.assertEqual(result, s)


if __name__ == '__main__':
    unittest.main()

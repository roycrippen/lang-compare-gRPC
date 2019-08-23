import time

import yaml
import grpc
# from grpc._channel import _Rendezvous

import lang_compare_pb2_grpc
import lang_compare_pb2


def xor_cipher(key: str, in_str: str) -> str:
    key_len = len(key)
    ks = bytearray(key, encoding='utf-8')
    xs = bytearray()
    for i, c in enumerate(bytearray(in_str, encoding='utf-8')):
        xs.append(c ^ ks[i % key_len])
    return xs.decode()


# noinspection PyBroadException
def connect_server(port):
    port_str = 'localhost:{}'.format(port)
    channel = grpc.insecure_channel(port_str)
    stub = lang_compare_pb2_grpc.LangCompareStub(channel)
    time.sleep(0.25)

    request = lang_compare_pb2.PingRequest()
    try:
        stub.Ping(request)
        return stub
    except Exception as _e:
        print("Could PING server on port {}".format(port))
        # raise e
        return None


def set_stub(lang, port):
    stub = connect_server(port)
    if stub is None:
        err_str = "\n  Could not connect to server (type, port): ({}, {})\n".format(lang, port)
        err_str += "  Try starting the server."
        raise RuntimeError(err_str)
    print("Connected to server (type, port): ({:4}, {})".format(lang, port))
    return stub


def read_config(file):
    with open(file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)


class Server:
    type = ""
    port = -1
    cmd = ""
    stub = None

    def __init__(self, dictionary):
        self.type = dictionary['type']
        self.port = dictionary['port']
        self.cmd = dictionary['cmd']

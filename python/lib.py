import time

import yaml
import grpc
# from grpc._channel import _Rendezvous

import lang_compare_pb2_grpc
import lang_compare_pb2


class Server:
    name = ""
    type = ""
    port = -1
    cmd = ""
    stub = None

    def __init__(self, name, dictionary):
        self.name = name
        self.type = dictionary['type']
        self.port = dictionary['port']
        self.cmd = dictionary['cmd']


def xor_cipher(key: str, in_str: str) -> str:
    key_len = len(key)
    ks = bytearray(key, encoding='utf-8')
    xs = bytearray()
    for i, c in enumerate(bytearray(in_str, encoding='utf-8')):
        xs.append(c ^ ks[i % key_len])
    return xs.decode()


# noinspection PyBroadException
def connect_server(script_name, server: Server):
    port_str = 'localhost:{}'.format(server.port)
    channel = grpc.insecure_channel(port_str)
    stub = lang_compare_pb2_grpc.LangCompareStub(channel)
    time.sleep(0.25)

    request = lang_compare_pb2.PingRequest(in_str=script_name)
    try:
        stub.Ping(request)
        return stub
    except Exception as _e:
        print("Could not PING server on port {}".format(server.port))
        # raise e
        return None


def set_stub(script_name, server: Server):
    server_str = "server (type, port, name): ({:5}, {}, {})\n".format(server.type, server.port, server.name)
    stub = connect_server(script_name, server)
    if stub is None:
        err_str = "\n  Could not connect to " + server_str + "\n  Try starting the server."
        raise RuntimeError(err_str)
    print("Connected to " + server_str)
    return stub


def read_config(file):
    with open(file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)


def load_server_stubs(script_name, file):
    config = read_config('config.yaml')
    servers = {}
    for k, v in config['servers'].items():
        servers[k] = Server(k, v)
        servers[k].stub = set_stub(script_name, servers[k])
    return servers

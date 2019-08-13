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

    request = lang_compare_pb2.PingRequest()
    try:
        stub.Ping(request)
    except Exception as e:
        print("Could not connect to server on port {}".format(port))
        raise e

    return stub

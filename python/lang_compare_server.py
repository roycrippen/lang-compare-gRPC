from concurrent import futures
import time
import logging

import grpc

import lang_compare_pb2
import lang_compare_pb2_grpc
import lib

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class LangCompare(lang_compare_pb2_grpc.LangCompareServicer):
    def XorCipher(self, request, context):
        return lang_compare_pb2.XorCipherReply(out_str=lib.xor_cipher(request.in_str, request.key))


def serve():
    port = 'localhost:50052'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lang_compare_pb2_grpc.add_LangCompareServicer_to_server(LangCompare(), server)
    print("Python lang-compare server listening on: {}".format(port))
    server.add_insecure_port(port)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def tester():
    cs = "message"
    key = "my key"
    encrypted = lib.xor_cipher(cs, key)
    decrypted = lib.xor_cipher(encrypted, key)
    print("key: {}".format(key))
    print("input string    : '{}'".format(cs))
    print("encrypted string: {}".format(bytes(encrypted, encoding='utf-8')))
    print("encrypted bytes : '{}'".format(list(bytes(encrypted, encoding='utf-8'))))
    print("decrypted string: '{}'".format(decrypted))


if __name__ == '__main__':
    # tester()
    logging.basicConfig()
    serve()

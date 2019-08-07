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
        return lang_compare_pb2.XorCipherReply(out_str=lib.xor_cipher(request.key, request.in_str))


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


if __name__ == '__main__':
    logging.basicConfig()
    serve()

from concurrent import futures
import time
import logging
import sys

import grpc

import lang_compare_pb2
import lang_compare_pb2_grpc
import lib

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class LangCompare(lang_compare_pb2_grpc.LangCompareServicer):
    xor_cnt = 0

    def XorCipher(self, request, _context):
        logging.debug("call to lib.xor_cipher, key='{}', in_str length = '{},".format(request.key, len(request.in_str)))
        self.xor_cnt += 1
        return lang_compare_pb2.XorCipherReply(out_str=lib.xor_cipher(request.key, request.in_str))

    def Ping(self, request, context):
        logging.info('Ping received.')
        return lang_compare_pb2.Pong()


def serve():
    port_str = 'localhost:50052'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lang_compare = LangCompare()
    lang_compare_pb2_grpc.add_LangCompareServicer_to_server(lang_compare, server)
    port = server.add_insecure_port(port_str)
    if port == 0:
        logging.error("Could not connect to server at port {}".format(port_str))
    else:
        server.start()
        msg_str = "Python lang-compare server listening on: {}".format(port_str)
        logging.info(msg_str)
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)
            logging.info("xor_cipher call count: {:,} ".format(lang_compare.xor_cnt))
            logging.info("Server stopped on port: {} ".format(port_str))


def set_logger():
    # file logging
    fmt_str = '[%(levelname)s:%(name)s] -> %(message)s'
    logging.basicConfig(filename='lang-compare-server.log', filemode='w', level=logging.INFO, format=fmt_str)
    root = logging.getLogger()

    # console logging
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(fmt_str))
    root.addHandler(handler)

    return root


if __name__ == '__main__':
    root_logger = set_logger()
    serve()

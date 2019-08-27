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

    def XorCipher(self, request, _context):
        # logging.debug("lib.xor_cipher, key='{}', in_str length = '{},".format(request.key, len(request.in_str)))
        return lang_compare_pb2.XorCipherReply(out_str=lib.xor_cipher(request.key, request.in_str))

    def Ping(self, request, _context):
        logging.info('Ping received from: {}'.format(request.in_str))
        return lang_compare_pb2.Pong()


def serve(port_num):
    port_str = 'localhost:{}'.format(port_num)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lang_compare = LangCompare()
    lang_compare_pb2_grpc.add_LangCompareServicer_to_server(lang_compare, server)
    port_num = server.add_insecure_port(port_str)
    if port_num == 0:
        err_str = "Could not connect to server at port {}".format(port_str)
        logging.error(err_str)
        raise RuntimeError(err_str)
    else:
        server.start()
        msg_str = "Server listening on: {}".format(port_str)
        logging.info(msg_str)
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)


def set_logger(filename=None):
    fmt_str = '[%(levelname)s:Py  Server] -> %(message)s'

    if filename is not None:  # file and stdout
        logging.basicConfig(filename=filename, filemode='w', level=logging.INFO, format=fmt_str)
        logging.basicConfig(level=logging.INFO, format=fmt_str)
        root = logging.getLogger()
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(fmt_str))
        root.addHandler(handler)
    else:
        logging.basicConfig(level=logging.INFO, format=fmt_str)
        root = logging.getLogger()

    return root


if __name__ == '__main__':
    root_logger = set_logger()
    config = lib.read_config('config.yaml')
    port = 50051
    if 'servers' in config and 'py' in config['servers'] and 'port' in config['servers']['py']:
        port = config['servers']['py']['port']
    serve(port)

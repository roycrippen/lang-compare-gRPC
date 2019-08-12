# python lang-compare-gRPC

depends on grpcio, grpcio-tools, hypothesis and pyyaml

### install dependencies
```bash
$ pip3 install grpcio --user
$ pip3 install grpcio-tools --user
$ pip3 install hypothesis --user
$ pip3 install pyyaml --user
```

### compile proto
```bash
# command creates:
#    lang_compare_pb2.py
#    lang_compare_pb2_grpc.py
$ python3 -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/lang_compare.proto
```

### start server in separate terminal
```bash
$ python3 lang_compare_server.py 
```

### then run client tests
```bash
$ python3 lang_compare_client_tests.py  
```

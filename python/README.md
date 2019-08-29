# python lang-compare-gRPC

depends on grpcio, grpcio-tools, hypothesis and pyyaml

also see [cpp dependencies](../cpp/README.md)
and see [rust dependencies](../rust/README.md)

cpp and rust servers need to be built

### install dependencies
```bash
$ pip3 install grpcio --user
$ pip3 install grpcio-tools --user
$ pip3 install hypothesis --user
$ pip3 install pyyaml --user
```

### compile proto file
* after cloning the repository
* and every time ../protos/lang_compare.proto is updated.
```bash
# command creates:
#    lang_compare_pb2.py
#    lang_compare_pb2_grpc.py
$ python3 -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/lang_compare.proto
 
# or
$ bash build_pb2.sh
```

### start severs (each in new terminal)
##### start python server
```bash
$ python3 server_example.py 
```

##### start cpp server
```bash
$ ../cpp/server_example 
```

##### start rust server
```bash
$ cd rust
$ cargo run --bin example-server --release
```

##### run all tests
```bash
# start all servers
# make changes to config.yaml as needed 
# then run the tests
$ python3 client_example.py
```

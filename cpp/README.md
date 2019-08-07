# cpp lang-compare-gRPC

depends on [gRPC](https://github.com/grpc/grpc) and [protoc](https://github.com/protocolbuffers/protobuf)

go [here](https://github.com/grpc/grpc/blob/master/BUILDING.md) for gRPC detailed install instructions

### install dependencies (Ubuntu)
```bash
# build dependencies
$ sudo apt-get install build-essential autoconf libtool pkg-config

# clone repositories
$ git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc
$ cd grpc
$ git submodule update --init

# make gRPC (this will also make protoc)
$ make

# install
$ sudo make install
$ cd third_party/protobuf
$ sudo make install

# add PKG_CONFIG_PATH to .bash.rc 
$ export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig"
```

### build 
```bash
# get into this directory
$ cd lang-compare-gpc/cpp

# clean
$ make clean

# build 
$ make
```

### run server
```bash
# start server
$ ./lang_compare_server
```

### run test client (new terminal)
```bash
# run client tests
$ ./lang_compare_client_tests
```

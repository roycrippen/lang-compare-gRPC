# cpp lang-compare-gRPC

depends on [gRPC](https://github.com/grpc/grpc) and [protoc](https://github.com/protocolbuffers/protobuf)

option dependency [compiledb](https://github.com/nickdiego/compiledb)

go [here](https://github.com/grpc/grpc/blob/master/BUILDING.md) for gRPC detailed install instructions

also see [python project](../python/README.md)


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

### build server
```bash
# get into this directory
$ cd lang-compare-gpc/cpp

# clean
$ make clean

# build 
$ make
```

### start server
```bash
# start server
$ ./server_example
```

### run server test (in new terminal)
```bash
# run server test
$ ./test_cpp_server
```

### install compiledb 
```bash
$ pip3 install compiledb --user
```

### create/update compile_commands.json
```bash
$ compiledb -n make
```
open compile_commands.json as a project in [clion](https://www.jetbrains.com/help/clion/compilation-database.html)

run this command anytime Makefile changes


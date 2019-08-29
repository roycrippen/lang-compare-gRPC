# rust lang-compare-gRPC

depends on [rust installed with rustup](https://rustup.rs)

### build server and test client
```bash
# get into this directory
$ cd lang-compare-gpc/rust

cargo build --release
```

### start server
```bash
# start server
$ cargo run --bin example-server --release
```

### run test client (in new terminal)
```bash
# run test client
$ cargo run --bin example-client --release
```

### run unit tests 
```bash
$ cargo test --release
```

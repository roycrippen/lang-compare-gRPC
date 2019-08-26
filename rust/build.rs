fn main() {
    // Build lang_compare
    tower_grpc_build::Config::new()
        .enable_server(true)
        .enable_client(true)
        .build(
            &["../protos/lang_compare.proto"],
            &["../protos"],
        )
        .unwrap_or_else(|e| panic!("protobuf compilation failed: {}", e));
    println!("cargo:rerun-if-changed=protos/lang_compare.proto");
}

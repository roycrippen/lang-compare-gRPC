use std::fs;
use std::env;

fn main() {
    // Build lang_compare
    tower_grpc_build::Config::new()
        .enable_server(true)
        .enable_client(true)
        .build(
            &["../../protos/lang_compare.proto"],
            &["../../protos"],
        )
        .unwrap_or_else(|e| panic!("protobuf compilation failed: {}", e));
    println!("cargo:rerun-if-changed=protos/lang_compare.proto");

    // move the generated to src
    let out_dir = env::var("OUT_DIR").unwrap();
    let generated_file = format!("{}/langcompare.rs", out_dir);
    fs::copy(generated_file, "../stub/src/langcompare.rs")
        .unwrap_or_else(|e| panic!("could not make a copy of generated file: {}", e));
}

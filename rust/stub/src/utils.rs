// use std::env::current_dir;
use std::fs::File;
use std::io::prelude::*;
use yaml_rust::yaml::Yaml;
use yaml_rust::YamlLoader;

pub fn read_config(file: &str) -> Yaml {
    // let dir = current_dir().unwrap();
    // println!("current_dir = {:?}", dir);
    // println!("input file = {:?}", file);
    let mut file = File::open(file).expect("Unable to open file");
    let mut contents = String::new();

    file.read_to_string(&mut contents)
        .expect("Unable to read file");

    let docs = YamlLoader::load_from_str(&contents).unwrap();
    let doc = &docs[0];

    return doc.clone();
}

pub fn get_server_port(file: &str) -> i64 {
    let doc = read_config(file);
    let port = doc["servers"]["rust_example"]["port"].as_i64().unwrap();
    port
}

pub fn xor_cipher(key: &str, in_str: &str) -> String {
    let ks = key.as_bytes();
    let xs = in_str
        .as_bytes()
        .iter()
        .enumerate()
        .map(|(i, &b)| b ^ ks[i % ks.len()])
        .collect::<Vec<u8>>();
    // let s = String::from_utf8(xs.clone()).unwrap();
    // println!("s = {:?}", s);
    String::from_utf8(xs).unwrap()
}

#[cfg(test)]
mod tests {
    #[test]
    fn read_port() {
        use crate::utils::read_config;

        let doc = read_config("../../python/config.yaml");
        let port = doc["servers"]["rust_example"]["port"].as_i64();
        assert!(port.is_some())
    }

    #[test]
    fn xor_cipher_twice() {
        use crate::utils::xor_cipher;

        let key = "test key";
        let msg = "this is a message";
        assert_eq!(msg, xor_cipher(key, &xor_cipher(key, msg)))
    }
}


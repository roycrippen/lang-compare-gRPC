#![deny(warnings, rust_2018_idioms)]

use futures::Future;
use hyper::client::connect::{Destination, HttpConnector};
use stub::utils::get_server_port;
use tower_grpc::Request;
use tower_hyper::{client, util};
use tower_util::MakeService;

use tokio::runtime::current_thread::Runtime;

fn call_xor_cipher(key: String, msg: String, uri: http::Uri) -> Result<String, ()> {
    let dst = Destination::try_from_uri(uri.clone()).unwrap();
    let connector = util::Connector::new(HttpConnector::new(4));
    let settings = client::Builder::new().http2_only(true).clone();
    let mut make_client = client::Connect::with_builder(connector, settings);

    let f = make_client
        .make_service(dst)
        .map_err(|e| panic!("connect error: {:?}", e))
        .and_then(move |conn| {
            use stub::langcompare::client::LangCompare;

            let conn = tower_request_modifier::Builder::new()
                .set_origin(uri)
                .build(conn)
                .unwrap();

            // Wait until the client is ready...
            LangCompare::new(conn).ready()
        })
        .and_then(|mut client| {
            use stub::langcompare::XorCipherRequest;

            client.xor_cipher(Request::new(XorCipherRequest {
                key: key.clone(),
                in_str: msg.clone(),
            }))
        })
        .and_then(|response| {
            let res = response.into_inner().out_str;
            Ok(res)
        })
        .map_err(|e| {
            println!("ERR = {:?}", e);
        });

    let mut runtime = Runtime::new().unwrap();
    let result = runtime.block_on(f);
    result
}

pub fn main() {
    let port = get_server_port("../python/config.yaml");
    let uri: http::Uri = format!("http://127.0.0.1:{}", port).parse().unwrap();
    println!("uri = {:?}", uri);

    let key = "some key".to_owned();
    let msg = "this is some message".to_owned();
    let result_first = call_xor_cipher(key.clone(), msg.clone(), uri.clone()).unwrap();
    let result = call_xor_cipher(key.clone(), result_first, uri).unwrap();
    println!("                original msg: '{}'", msg.clone());
    println!("xor_cipher applied twice msg: '{}'", result.clone());
    assert_eq!(msg, result)
}

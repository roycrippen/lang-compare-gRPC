#![deny(warnings, rust_2018_idioms)]


use futures::{future, Future, Stream};
use log::error;
use tokio::net::TcpListener;
use tower_grpc::{Request, Response};
use tower_hyper::server::{Http, Server};
use stub::langcompare::{server, XorCipherRequest, XorCipherReply, PingRequest, Pong};

#[derive(Clone, Debug)]
struct LC;

impl server::LangCompare for LC {
    // type names = rpc definition from proto + 'Future'
    type XorCipherFuture = future::FutureResult<Response<XorCipherReply>, tower_grpc::Status>;
    type PingFuture = future::FutureResult<Response<Pong>, tower_grpc::Status>;

    fn xor_cipher(&mut self, _request: Request<XorCipherRequest>) -> Self::XorCipherFuture {
        let response = Response::new(XorCipherReply {
            out_str: "xor reply".to_string(),
        });
        future::ok(response)
    }

    fn ping(&mut self, request: Request<PingRequest>) -> Self::PingFuture {
        println!("[INFO:Rust Server] -> Ping received from: {}", request.into_inner().in_str);
        let response = Response::new(Pong {});
        future::ok(response)
    }

}

pub fn main() {
    let _ = ::env_logger::init();

    let new_service = server::LangCompareServer::new(LC);

    let mut server = Server::new(new_service);

    let http = Http::new().http2_only(true).clone();

    // todo: read from config.yaml
    let addr = "127.0.0.1:50053".parse().unwrap();
    let bind = TcpListener::bind(&addr).expect("bind");

    let serve = bind
        .incoming()
        .for_each(move |sock| {
            if let Err(e) = sock.set_nodelay(true) {
                return Err(e);
            }

            let serve =  server.serve_with(sock, http.clone());
            tokio::spawn(serve.map_err(|e| error!("hyper error: {:?}", e)));
            Ok(())
        })
        .map_err(|e| eprintln!("accept error: {}", e));

    println!("[INFO:Rust Server] -> Server listening on: {}", addr);
    tokio::run(serve)
}

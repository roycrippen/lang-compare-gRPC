#![deny(warnings, rust_2018_idioms)]


use futures::{future, Future, Stream};
use log::error;
use tokio::net::TcpListener;
use tower_grpc::{Request, Response};
use tower_hyper::server::{Http, Server};
use stub::langcompare::{server, XorCipherRequest, XorCipherReply, PingRequest, Pong};
use stub::utils::{get_server_port, xor_cipher};


#[derive(Clone, Debug)]
struct LC;

impl server::LangCompare for LC {
    // type names = rpc definition from proto + 'Future'
    type XorCipherFuture = future::FutureResult<Response<XorCipherReply>, tower_grpc::Status>;
    type PingFuture = future::FutureResult<Response<Pong>, tower_grpc::Status>;

    fn xor_cipher(&mut self, request: Request<XorCipherRequest>) -> Self::XorCipherFuture {
        let r = request.into_inner();
        let response = Response::new(XorCipherReply {
            out_str: xor_cipher(&r.key, &r.in_str),
        });
        future::ok(response)
    }

    fn ping(&mut self, request: Request<PingRequest>) -> Self::PingFuture {
        println!(
            "[INFO:Rust Server] -> Ping received from: {}",
            request.into_inner().in_str
        );
        let response = Response::new(Pong {});
        future::ok(response)
    }
}

pub fn main() {
    let _ = ::env_logger::init();
    let new_service = server::LangCompareServer::new(LC);
    let mut server = Server::new(new_service);
    let http = Http::new().http2_only(true).clone();

    let port = get_server_port("../python/config.yaml");
    let addr = format!("127.0.0.1:{}", port).parse().unwrap();
    let bind = TcpListener::bind(&addr).expect("bind");

    let serve = bind
        .incoming()
        .for_each(move |sock| {
            if let Err(e) = sock.set_nodelay(true) {
                return Err(e);
            }

            let serve = server.serve_with(sock, http.clone());
            tokio::spawn(serve.map_err(|e| error!("hyper error: {:?}", e)));
            Ok(())
        })
        .map_err(|e| eprintln!("accept error: {}", e));

    println!("[INFO:Rust Server] -> Server listening on: {}", addr);
    tokio::run(serve)
}

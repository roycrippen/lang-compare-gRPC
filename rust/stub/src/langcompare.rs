/// XOR encryption key and in_str
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct XorCipherRequest {
    #[prost(string, tag="1")]
    pub key: std::string::String,
    #[prost(string, tag="2")]
    pub in_str: std::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct XorCipherReply {
    #[prost(string, tag="1")]
    pub out_str: std::string::String,
}
/// ping pong
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PingRequest {
    #[prost(string, tag="1")]
    pub in_str: std::string::String,
}
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Pong {
}
pub mod client {
    use ::tower_grpc::codegen::client::*;
    use super::{XorCipherRequest, XorCipherReply, PingRequest, Pong};

    /// Service definitions
    #[derive(Debug, Clone)]
    pub struct LangCompare<T> {
        inner: grpc::Grpc<T>,
    }

    impl<T> LangCompare<T> {
        pub fn new(inner: T) -> Self {
            let inner = grpc::Grpc::new(inner);
            Self { inner }
        }

        /// Poll whether this client is ready to send another request.
        pub fn poll_ready<R>(&mut self) -> futures::Poll<(), grpc::Status>
        where T: grpc::GrpcService<R>,
        {
            self.inner.poll_ready()
        }

        /// Get a `Future` of when this client is ready to send another request.
        pub fn ready<R>(self) -> impl futures::Future<Item = Self, Error = grpc::Status>
        where T: grpc::GrpcService<R>,
        {
            futures::Future::map(self.inner.ready(), |inner| Self { inner })
        }

        /// Service definitions
        pub fn xor_cipher<R>(&mut self, request: grpc::Request<XorCipherRequest>) -> grpc::unary::ResponseFuture<XorCipherReply, T::Future, T::ResponseBody>
        where T: grpc::GrpcService<R>,
              grpc::unary::Once<XorCipherRequest>: grpc::Encodable<R>,
        {
            let path = http::PathAndQuery::from_static("/langcompare.LangCompare/XorCipher");
            self.inner.unary(request, path)
        }

        /// Service definitions
        pub fn ping<R>(&mut self, request: grpc::Request<PingRequest>) -> grpc::unary::ResponseFuture<Pong, T::Future, T::ResponseBody>
        where T: grpc::GrpcService<R>,
              grpc::unary::Once<PingRequest>: grpc::Encodable<R>,
        {
            let path = http::PathAndQuery::from_static("/langcompare.LangCompare/Ping");
            self.inner.unary(request, path)
        }
    }
}

pub mod server {
    use ::tower_grpc::codegen::server::*;
    use super::{XorCipherRequest, XorCipherReply, PingRequest, Pong};

    // Redefine the try_ready macro so that it doesn't need to be explicitly
    // imported by the user of this generated code.
    macro_rules! try_ready {
        ($e:expr) => (match $e {
            Ok(futures::Async::Ready(t)) => t,
            Ok(futures::Async::NotReady) => return Ok(futures::Async::NotReady),
            Err(e) => return Err(From::from(e)),
        })
    }

    /// Service definitions
    pub trait LangCompare: Clone {
        type XorCipherFuture: futures::Future<Item = grpc::Response<XorCipherReply>, Error = grpc::Status>;
        type PingFuture: futures::Future<Item = grpc::Response<Pong>, Error = grpc::Status>;

        fn xor_cipher(&mut self, request: grpc::Request<XorCipherRequest>) -> Self::XorCipherFuture;

        fn ping(&mut self, request: grpc::Request<PingRequest>) -> Self::PingFuture;
    }

    #[derive(Debug, Clone)]
    pub struct LangCompareServer<T> {
        lang_compare: T,
    }

    impl<T> LangCompareServer<T>
    where T: LangCompare,
    {
        pub fn new(lang_compare: T) -> Self {
            Self { lang_compare }
        }
    }

    impl<T> tower::Service<http::Request<grpc::BoxBody>> for LangCompareServer<T>
    where T: LangCompare,
    {
        type Response = http::Response<lang_compare::ResponseBody<T>>;
        type Error = grpc::Never;
        type Future = lang_compare::ResponseFuture<T>;

        fn poll_ready(&mut self) -> futures::Poll<(), Self::Error> {
            Ok(().into())
        }

        fn call(&mut self, request: http::Request<grpc::BoxBody>) -> Self::Future {
            use self::lang_compare::Kind::*;

            match request.uri().path() {
                "/langcompare.LangCompare/XorCipher" => {
                    let service = lang_compare::methods::XorCipher(self.lang_compare.clone());
                    let response = grpc::unary(service, request);
                    lang_compare::ResponseFuture { kind: XorCipher(response) }
                }
                "/langcompare.LangCompare/Ping" => {
                    let service = lang_compare::methods::Ping(self.lang_compare.clone());
                    let response = grpc::unary(service, request);
                    lang_compare::ResponseFuture { kind: Ping(response) }
                }
                _ => {
                    lang_compare::ResponseFuture { kind: __Generated__Unimplemented(grpc::unimplemented(format!("unknown service: {:?}", request.uri().path()))) }
                }
            }
        }
    }

    impl<T> tower::Service<()> for LangCompareServer<T>
    where T: LangCompare,
    {
        type Response = Self;
        type Error = grpc::Never;
        type Future = futures::FutureResult<Self::Response, Self::Error>;

        fn poll_ready(&mut self) -> futures::Poll<(), Self::Error> {
            Ok(futures::Async::Ready(()))
        }

        fn call(&mut self, _target: ()) -> Self::Future {
            futures::ok(self.clone())
        }
    }

    impl<T> tower::Service<http::Request<tower_hyper::Body>> for LangCompareServer<T>
    where T: LangCompare,
    {
        type Response = <Self as tower::Service<http::Request<grpc::BoxBody>>>::Response;
        type Error = <Self as tower::Service<http::Request<grpc::BoxBody>>>::Error;
        type Future = <Self as tower::Service<http::Request<grpc::BoxBody>>>::Future;

        fn poll_ready(&mut self) -> futures::Poll<(), Self::Error> {
            tower::Service::<http::Request<grpc::BoxBody>>::poll_ready(self)
        }

        fn call(&mut self, request: http::Request<tower_hyper::Body>) -> Self::Future {
            let request = request.map(|b| grpc::BoxBody::map_from(b));
            tower::Service::<http::Request<grpc::BoxBody>>::call(self, request)
        }
    }

    pub mod lang_compare {
        use ::tower_grpc::codegen::server::*;
        use super::LangCompare;
        use super::super::{XorCipherRequest, PingRequest};

        pub struct ResponseFuture<T>
        where T: LangCompare,
        {
            pub(super) kind: Kind<
                // XorCipher
                grpc::unary::ResponseFuture<methods::XorCipher<T>, grpc::BoxBody, XorCipherRequest>,
                // Ping
                grpc::unary::ResponseFuture<methods::Ping<T>, grpc::BoxBody, PingRequest>,
                // A generated catch-all for unimplemented service calls
                grpc::unimplemented::ResponseFuture,
            >,
        }

        impl<T> futures::Future for ResponseFuture<T>
        where T: LangCompare,
        {
            type Item = http::Response<ResponseBody<T>>;
            type Error = grpc::Never;

            fn poll(&mut self) -> futures::Poll<Self::Item, Self::Error> {
                use self::Kind::*;

                match self.kind {
                    XorCipher(ref mut fut) => {
                        let response = try_ready!(fut.poll());
                        let response = response.map(|body| {
                            ResponseBody { kind: XorCipher(body) }
                        });
                        Ok(response.into())
                    }
                    Ping(ref mut fut) => {
                        let response = try_ready!(fut.poll());
                        let response = response.map(|body| {
                            ResponseBody { kind: Ping(body) }
                        });
                        Ok(response.into())
                    }
                    __Generated__Unimplemented(ref mut fut) => {
                        let response = try_ready!(fut.poll());
                        let response = response.map(|body| {
                            ResponseBody { kind: __Generated__Unimplemented(body) }
                        });
                        Ok(response.into())
                    }
                }
            }
        }

        pub struct ResponseBody<T>
        where T: LangCompare,
        {
            pub(super) kind: Kind<
                // XorCipher
                grpc::Encode<grpc::unary::Once<<methods::XorCipher<T> as grpc::UnaryService<XorCipherRequest>>::Response>>,
                // Ping
                grpc::Encode<grpc::unary::Once<<methods::Ping<T> as grpc::UnaryService<PingRequest>>::Response>>,
                // A generated catch-all for unimplemented service calls
                (),
            >,
        }

        impl<T> tower::HttpBody for ResponseBody<T>
        where T: LangCompare,
        {
            type Data = <grpc::BoxBody as grpc::Body>::Data;
            type Error = grpc::Status;

            fn is_end_stream(&self) -> bool {
                use self::Kind::*;

                match self.kind {
                    XorCipher(ref v) => v.is_end_stream(),
                    Ping(ref v) => v.is_end_stream(),
                    __Generated__Unimplemented(_) => true,
                }
            }

            fn poll_data(&mut self) -> futures::Poll<Option<Self::Data>, Self::Error> {
                use self::Kind::*;

                match self.kind {
                    XorCipher(ref mut v) => v.poll_data(),
                    Ping(ref mut v) => v.poll_data(),
                    __Generated__Unimplemented(_) => Ok(None.into()),
                }
            }

            fn poll_trailers(&mut self) -> futures::Poll<Option<http::HeaderMap>, Self::Error> {
                use self::Kind::*;

                match self.kind {
                    XorCipher(ref mut v) => v.poll_trailers(),
                    Ping(ref mut v) => v.poll_trailers(),
                    __Generated__Unimplemented(_) => Ok(None.into()),
                }
            }
        }

        #[allow(non_camel_case_types)]
        #[derive(Debug, Clone)]
        pub(super) enum Kind<XorCipher, Ping, __Generated__Unimplemented> {
            XorCipher(XorCipher),
            Ping(Ping),
            __Generated__Unimplemented(__Generated__Unimplemented),
        }

        pub mod methods {
            use ::tower_grpc::codegen::server::*;
            use super::super::{LangCompare, XorCipherRequest, XorCipherReply, PingRequest, Pong};

            pub struct XorCipher<T>(pub T);

            impl<T> tower::Service<grpc::Request<XorCipherRequest>> for XorCipher<T>
            where T: LangCompare,
            {
                type Response = grpc::Response<XorCipherReply>;
                type Error = grpc::Status;
                type Future = T::XorCipherFuture;

                fn poll_ready(&mut self) -> futures::Poll<(), Self::Error> {
                    Ok(futures::Async::Ready(()))
                }

                fn call(&mut self, request: grpc::Request<XorCipherRequest>) -> Self::Future {
                    self.0.xor_cipher(request)
                }
            }

            pub struct Ping<T>(pub T);

            impl<T> tower::Service<grpc::Request<PingRequest>> for Ping<T>
            where T: LangCompare,
            {
                type Response = grpc::Response<Pong>;
                type Error = grpc::Status;
                type Future = T::PingFuture;

                fn poll_ready(&mut self) -> futures::Poll<(), Self::Error> {
                    Ok(futures::Async::Ready(()))
                }

                fn call(&mut self, request: grpc::Request<PingRequest>) -> Self::Future {
                    self.0.ping(request)
                }
            }
        }
    }
}

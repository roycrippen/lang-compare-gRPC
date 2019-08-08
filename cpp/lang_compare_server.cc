#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "lang_compare.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using langcompare::XorCipherRequest;
using langcompare::XorCipherReply;
using langcompare::LangCompare;

using namespace std;

string applyXorCipher(string const &key, string const &cs) {
    string res = cs;
    auto mod = key.size() / sizeof(char);
    for (u_long i = 0; i < cs.size(); i++) {
        auto c = key[i % mod];
        res[i] = cs[i] ^ c;
    }
    return res;
}


// Logic and data behind the server's behavior.
class LangCompareServiceImpl final : public LangCompare::Service {
    Status XorCipher(ServerContext* context, const XorCipherRequest* request, XorCipherReply* reply) override {
        auto res = applyXorCipher(request->key(), request->in_str());
        reply->set_out_str(res);
        return Status::OK;
    }
};

void RunServer() {
  string server_address("0.0.0.0:50051");
  LangCompareServiceImpl service;

  ServerBuilder builder;

  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());

  // Register "service" as the instance through which we'll communicate with clients.
  builder.RegisterService(&service);

  // Finally assemble the server.
  unique_ptr<Server> server(builder.BuildAndStart());
  cout << "C++ lang-compare Server listening on " << server_address << endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char** argv) {
  RunServer();

  return 0;
}

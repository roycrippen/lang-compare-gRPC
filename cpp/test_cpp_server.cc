#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "lang_compare.grpc.pb.h"

using namespace std;

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

using langcompare::PingRequest;
using langcompare::Pong;
using langcompare::XorCipherRequest;
using langcompare::XorCipherReply;
using langcompare::LangCompare;

class LangCompareClient {
public:
    explicit LangCompareClient(const shared_ptr<Channel>& channel)
            : stub_(LangCompare::NewStub(channel)) {}

    // Assembles the client's payload, sends it and presents the response back
    // from the server.
    string xorCipher(const string &key, const string &in_str) {
        // Data we are sending to the server.
        XorCipherRequest request;
        request.set_key(key);
        request.set_in_str(in_str);

        // Container for the data we expect from the server.
        XorCipherReply reply;

        // Context for the client. It could be used to convey extra information to
        // the server and/or tweak certain RPC behaviors.
        ClientContext context;

        // The actual RPC.
        Status status = stub_->XorCipher(&context, request, &reply);

        // Act upon its status.
        auto res = status.ok() ? reply.out_str() : "xorCipher(...) call failed.";
        return res;
    }

    bool ping() {
        // Data we are sending to the server.
        PingRequest request;

        // Container for the data we expect from the server.
        Pong reply;

        // Context for the client. It could be used to convey extra information to
        // the server and/or tweak certain RPC behaviors.
        ClientContext context;

        // The actual RPC.
        Status status = stub_->Ping(&context, request, &reply);
        return status.ok();
    }

private:
    unique_ptr<LangCompare::Stub> stub_;
};

void test_xor_cipher_cpp(string port) {
    LangCompareClient compare(grpc::CreateChannel("localhost:" + port, grpc::InsecureChannelCredentials()));
    if (!compare.ping()) {
        cout << "Ping of server failed, aborting." << "\n";
        return;
    }

    int num = 1000;
    cout << "calling cpp xor_cipher " << num * 2 << " times" << endl;
    auto key = "my key";
    for (int i = 0; i < num - 1; ++i) {
        string in_str("message");
        in_str += to_string(num);
        string encrypted_reply = compare.xorCipher(key, in_str);
        string decrypted_reply = compare.xorCipher(key, encrypted_reply);
        assert(in_str == decrypted_reply);
    }
    string in_str("message");
    in_str += to_string(num - 1);
    string encrypted_reply = compare.xorCipher(key, in_str);
    string decrypted_reply = compare.xorCipher(key, encrypted_reply);
    cout << "last message: " << decrypted_reply << endl;
    assert(in_str == decrypted_reply);
}

int main(int argc, char **argv) {
    test_xor_cipher_cpp("50052");

    return 0;
}

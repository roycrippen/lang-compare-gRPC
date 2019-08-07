
#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>
#include "lang_compare.grpc.pb.h"

using namespace std;

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;

using langcompare::XorCipherRequest;
using langcompare::XorCipherReply;
using langcompare::LangCompare;

class LangCompareClient {
public:
    LangCompareClient(shared_ptr <Channel> channel)
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
        if (status.ok()) {
            return reply.out_str();
        } else {
            cout << status.error_code() << ": " << status.error_message() << endl;
            return "RPC failed";
        }
    }

private:
    unique_ptr <LangCompare::Stub> stub_;
};

void test_xor_cipher_cpp() {
    LangCompareClient compare(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
    int num = 1000;
    cout << "calling cpp xor_cipher " << num * 2 << " time" << endl;
    auto key = "my key";
    for (int i = 0; i < num - 1; ++i) {
        string in_str("message");
        in_str+= to_string(num);
        string encrypted_reply = compare.xorCipher(key, in_str);
        string decrypted_reply = compare.xorCipher(key, encrypted_reply);
    }
    string in_str("message");
    in_str+= to_string(num - 1);
    string encrypted_reply = compare.xorCipher(key, in_str);
    string decrypted_reply = compare.xorCipher(key, encrypted_reply);
    cout << "last message: " << decrypted_reply << endl;
}

int main(int argc, char **argv) {
    test_xor_cipher_cpp();

    return 0;
}

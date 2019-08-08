#include <string>

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
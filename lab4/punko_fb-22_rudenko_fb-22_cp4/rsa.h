#include "headers.h"

class RSA;
struct RSAKey;

struct RSAKey {
    mpz_class e; 
    mpz_class d; 
    mpz_class n; 

    std::string serializePublic() const { return e.get_str() + ":" + n.get_str(); }
    
    static std::pair<mpz_class, mpz_class> deserializePublic(const std::string& serialized);
};

class RSA {
private:
    static mpz_class gcd(const mpz_class& a, const mpz_class& b);
    static mpz_class modInverse(const mpz_class& e, const mpz_class& phi);
public:
    static RSAKey generateKeys(const mpz_class& p, const mpz_class& q);
    static mpz_class encrypt(const mpz_class& message, const mpz_class& e, const mpz_class& n);
    static mpz_class decrypt(const mpz_class& ciphertext, const mpz_class& d, const mpz_class& n);
    static mpz_class sign(const mpz_class& message, const mpz_class& d, const mpz_class& n);
    static bool verify(const mpz_class& message, const mpz_class& signature, const mpz_class& e, const mpz_class& n);
};

class Participant {
private:
    RSAKey keys;
    std::string name;
    mpz_class partner_e;
    mpz_class partner_n;

public:
    Participant(const std::string& name, const mpz_class& p, const mpz_class& q) : name(name) { keys = RSA::generateKeys(p, q); }

    std::string getPublicKey() const { return keys.serializePublic(); }
    const RSAKey& getKeys() const { return keys; }
    const std::string& getName() const { return name; }

    void setPartnerKey(const std::string& partnerKey);
    mpz_class sendKey(const mpz_class& shared_key);
    mpz_class receiveKey(const mpz_class& encrypted_shared_key);
    std::pair<mpz_class, mpz_class> sendMessage(const mpz_class& message);
    std::pair<mpz_class, bool> receiveMessage(const mpz_class& encrypted_message, const mpz_class& signature, const mpz_class& sender_e, const mpz_class& sender_n);
};
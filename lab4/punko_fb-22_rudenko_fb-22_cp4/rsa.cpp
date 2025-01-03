#include "rsa.h"

std::pair<mpz_class, mpz_class> RSAKey::deserializePublic(const std::string& serialized) {
    size_t delimiter = serialized.find(':');
    if (delimiter == std::string::npos) {
        throw std::runtime_error("Invalid key format");
    }
    return {
        mpz_class(serialized.substr(0, delimiter)),
        mpz_class(serialized.substr(delimiter + 1))
    };
}

mpz_class RSA::gcd(const mpz_class& a, const mpz_class& b) {
    mpz_class x = a, y = b;
    while (y != 0) {
        mpz_class temp = y;
        y = x % y;
        x = temp;
    }
    return x;
}

mpz_class RSA::modInverse(const mpz_class& e, const mpz_class& phi) {
    mpz_class old_r = e, r = phi;
    mpz_class old_s = 1, s = 0;
    mpz_class old_t = 0, t = 1;
        
    while (r != 0) {
        mpz_class quotient = old_r / r;
        mpz_class temp = r;
        r = old_r - quotient * r;
        old_r = temp;
            
        temp = s;
        s = old_s - quotient * s;
        old_s = temp;
            
        temp = t;
        t = old_t - quotient * t;
        old_t = temp;
    }
        
    if (old_s < 0) old_s += phi;
    return old_s;
}

RSAKey RSA::generateKeys(const mpz_class& p, const mpz_class& q) {
    RSAKey keys;
    keys.n = p * q;
    mpz_class phi = (p - 1) * (q - 1);
        
    keys.e = 65537;
    while (gcd(keys.e, phi) != 1) {
        keys.e += 2;
    }
        
    keys.d = modInverse(keys.e, phi);
        
    return keys;
}

mpz_class RSA::encrypt(const mpz_class& message, const mpz_class& e, const mpz_class& n) {
    mpz_class result;
    mpz_powm(result.get_mpz_t(), message.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
    return result;
}

mpz_class RSA::decrypt(const mpz_class& ciphertext, const mpz_class& d, const mpz_class& n) {
    mpz_class result;
    mpz_powm(result.get_mpz_t(), ciphertext.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());
    return result;
}   

mpz_class RSA::sign(const mpz_class& message, const mpz_class& d, const mpz_class& n) {
    mpz_class signature;
    mpz_powm(signature.get_mpz_t(), message.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());
    return signature;
}

bool RSA::verify(const mpz_class& message, const mpz_class& signature, const mpz_class& e, const mpz_class& n) {
    mpz_class decrypted;
    mpz_powm(decrypted.get_mpz_t(), signature.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
    return decrypted == message;
}

void Participant::setPartnerKey(const std::string& partnerKey) {
    auto [e, n] = RSAKey::deserializePublic(partnerKey);
    partner_e = e;
    partner_n = n;
}

std::pair<mpz_class, mpz_class> Participant::sendMessage(const mpz_class& message) {
    mpz_class signature = RSA::sign(message, keys.d, keys.n);
    mpz_class encrypted = RSA::encrypt(message, partner_e, partner_n);
    return {encrypted, signature};
}

std::pair<mpz_class, bool> Participant::receiveMessage(
    const mpz_class& encrypted_message, 
    const mpz_class& signature,
    const mpz_class& sender_e,
    const mpz_class& sender_n) {
        
    mpz_class decrypted = RSA::decrypt(encrypted_message, keys.d, keys.n);
    bool is_valid = RSA::verify(decrypted, signature, sender_e, sender_n);
        
    return {decrypted, is_valid};
}

mpz_class Participant::sendKey(const mpz_class& shared_key) {
    return RSA::encrypt(shared_key, partner_e, partner_n);
}

mpz_class Participant::receiveKey(const mpz_class& encrypted_shared_key) {
    return RSA::decrypt(encrypted_shared_key, keys.d, keys.n);
}

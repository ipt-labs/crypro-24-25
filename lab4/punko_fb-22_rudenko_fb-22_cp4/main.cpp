#include "headers.h"
#include "prime_generator.h"
#include "rsa.h"

mpz_class generateRandomMessage() {
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_int_distribution<uint64_t> dist(1, 1000000);
    return mpz_class(dist(gen));
}

int main(int argc, const char* argv[]) {
    PrimeGenerator generator;
    Participant alice("Alice", generator.generatePrime(256), generator.generatePrime(256));
    Participant bob("Bob", generator.generatePrime(256), generator.generatePrime(256));

    std::cout << "=== Key Exchange ===\n";
    std::string alicePublicKey = alice.getPublicKey();
    std::string bobPublicKey = bob.getPublicKey();
    std::cout << "Alice's public key: " << alicePublicKey << "\n";
    std::cout << "Bob's public key: " << bobPublicKey << "\n\n";
    
    alice.setPartnerKey(bobPublicKey);
    bob.setPartnerKey(alicePublicKey);

    std::cout << "=== Shared Key Exchange ===\n";
    mpz_class sharedKey = generateRandomMessage();
    std::cout << "Original shared key: " << sharedKey << "\n";

    mpz_class encryptedSharedKey = alice.sendKey(sharedKey);
    std::cout << "Encrypted shared key: " << encryptedSharedKey << "\n";

    mpz_class receivedSharedKey = bob.receiveKey(encryptedSharedKey);
    std::cout << "Decrypted shared key: " << receivedSharedKey << "\n";
    std::cout << "Shared key exchange " 
              << (sharedKey == receivedSharedKey ? "successful" : "failed")
              << "\n\n";

    std::cout << "=== Message Exchange ===\n";
    mpz_class aliceMessage;
    mpz_class bobMessage;
    bool aliceMessageProvided = false;
    bool bobMessageProvided = false;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--alice" && i + 1 < argc) {
            aliceMessage = mpz_class(argv[++i]);
            aliceMessageProvided = true;
        } else if (arg == "--bob" && i + 1 < argc) {
            bobMessage = mpz_class(argv[++i]);
            bobMessageProvided = true;
        } else {
            std::cerr << "Unknown argument: " << arg << "\n";
            return 1;
        }
    }

    if (!aliceMessageProvided) aliceMessage = generateRandomMessage();
    if (!bobMessageProvided) bobMessage = generateRandomMessage();
    
    std::cout << "Alice's original message: " << aliceMessage << "\n";
    auto [encrypted1, signature1] = alice.sendMessage(aliceMessage);
    std::cout << "Encrypted message: " << encrypted1 << "\n";
    std::cout << "Signature: " << signature1 << "\n\n";

    auto [decrypted1, isValid1] = bob.receiveMessage(
        encrypted1, signature1,
        alice.getKeys().e, alice.getKeys().n
    );
    std::cout << "Bob received:\n"
              << "Decrypted message: " << decrypted1 << "\n"
              << "Signature valid: " << (isValid1 ? "Yes" : "No") << "\n\n";

    std::cout << "Bob's original message: " << bobMessage << "\n";
    auto [encrypted2, signature2] = bob.sendMessage(bobMessage);
    std::cout << "Encrypted message: " << encrypted2 << "\n";
    std::cout << "Signature: " << signature2 << "\n\n";

    auto [decrypted2, isValid2] = alice.receiveMessage(
        encrypted2, signature2,
        bob.getKeys().e, bob.getKeys().n
    );
    std::cout << "Alice received:\n"
              << "Decrypted message: " << decrypted2 << "\n"
              << "Signature valid: " << (isValid2 ? "Yes" : "No") << "\n";

    return 0;
}
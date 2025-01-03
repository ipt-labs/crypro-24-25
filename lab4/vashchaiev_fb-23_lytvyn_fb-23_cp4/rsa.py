import random
import rsa_gen_key as rgk
import rsa_crypt as rc

def SendKey(k, d, n, o_e, o_n):
    secret_S = rc.Sign(k, d, n)
    open_S = rc.Encrypt(secret_S, o_e, o_n)
    open_k = rc.Encrypt(k, o_e, o_n)

    return open_S, open_k

def ReceiveKey(open_S, open_k, d, n, o_e, o_n):
    secret_S = rc.Decrypt(open_S, d, n)
    secret_k = rc.Decrypt(open_k, d, n)

    if rc.Verify(secret_S, secret_k, o_e, o_n):
        return secret_k
    else:
        return False

if __name__ == "__main__":
    alice_msg = "Hello Bob!"
    alice_text = rc.txt2int(alice_msg)

    alice = rgk.GenerateKeyPair(256, 384)
    bob = rgk.GenerateKeyPair(384, 512)

    open_a_n, open_a_e = bob.n, bob.e
    open_b_n, open_b_e = alice.n, alice.e

    C_alice2bob = rc.Encrypt(alice_text, open_a_e, open_a_n)
    S_from_alice = rc.Sign(alice_text, alice.d, alice.n)

    gen_k = random.randint(0, alice.n - 1)
    print(f"Generated k: {gen_k}")

    open_alice_S, open_alice_k = SendKey(gen_k, alice.d, alice.n, open_a_e, open_a_n)

    bob_msg = "Hello Alice!"
    bob_text = rc.txt2int(bob_msg)

    k = ReceiveKey(open_alice_S, open_alice_k, bob.d, bob.n, open_b_e, open_b_n)
    if k is not False:
        print(f"Secret k from Alice: {k}")

    M_alice2bob = rc.Decrypt(C_alice2bob, bob.d, bob.n)
    print(f"[Bob] Alice's message: {rc.int2txt(M_alice2bob)}")

    if rc.Verify(S_from_alice, M_alice2bob, open_b_e, open_b_n):
        print("Alice's message wasn't tampered with")

    C_bob2alice = rc.Encrypt(bob_text, open_b_e, open_b_n)
    S_from_bob = rc.Sign(bob_text, bob.d, bob.n)

    print()

    M_bob2alice = rc.Decrypt(C_bob2alice, alice.d, alice.n)
    print(f"[Alice] Bob's message: {rc.int2txt(M_bob2alice)}")
    if rc.Verify(S_from_bob, M_bob2alice, open_a_e, open_a_n):
            print("Bob's message wasn't tampered with")

    print("\n*** Results ***\n" + "-" * 30)

    print("ALICE:\n" + "-" * 10)

    print(f"Text: {alice_msg}")
    print(f"Secret p: {alice.p}")
    print(f"Secret q: {alice.q}")
    print(f"Secret d: {alice.d}")
    print(f"Open n: {alice.n}")
    print(f"Open e: {alice.e}")
    print(f"Signature: {S_from_alice}")

    print("\nHex format:")
    print(f"Text: {hex(alice_text)}")
    print(f"Secret p: {hex(alice.p)}")
    print(f"Secret q: {hex(alice.q)}")
    print(f"Secret d: {hex(alice.d)}")
    print(f"Open n: {hex(alice.n)}")
    print(f"Open e: {hex(alice.e)}")
    print(f"Signature: {hex(S_from_alice)}")

    print("\nBOB:\n" + "-" * 10)

    print(f"Text: {bob_msg}")
    print(f"Secret p: {bob.p}")
    print(f"Secret q: {bob.q}")
    print(f"Secret d: {bob.d}")
    print(f"Open n: {bob.n}")
    print(f"Open e: {bob.e}")
    print(f"Signature: {S_from_bob}")

    print("\nHex format:")
    print(f"Text: {hex(bob_text)}")
    print(f"Secret p: {hex(bob.p)}")
    print(f"Secret q: {hex(bob.q)}")
    print(f"Secret d: {hex(bob.d)}")
    print(f"Open n: {hex(bob.n)}")
    print(f"Open e: {hex(bob.e)}")
    print(f"Signature: {hex(S_from_bob)}")
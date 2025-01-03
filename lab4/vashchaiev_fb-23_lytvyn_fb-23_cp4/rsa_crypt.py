import json
import random
import prime_number as pn

class Import_key():
    def __init__(self, name):
        with open("keys.json", "r") as f:
            root = json.load(f)
        status = False
        for obj in root:
            if obj["name"] == name:
                self.d = int(obj["my_keys"]["d"], 16)
                self.p = int(obj["my_keys"]["p"], 16)
                self.q = int(obj["my_keys"]["q"], 16)
                self.n = int(obj["my_keys"]["n"], 16)
                self.e = int(obj["my_keys"]["e"], 16)
                self.o_n = int(obj["open_for_me"]["n"], 16)
                self.o_e = int(obj["open_for_me"]["e"], 16)
                status = True
                break
        if not status:
            raise KeyError("Not found keys for " + name)

def Encrypt(M, e, n):
    return pn._pow(M, e, n)

def Decrypt(C, d, n):
    return pn._pow(C, d, n)
 
def Sign(M, d, n):
    return pn._pow(M, d, n) # S

def Verify(S, M, e, n):
    return pn._pow(S, e, n) == M

def txt2int(text):
    return int(''.join(f"{ord(c):08b}" for c in text), 2)

def int2txt(number):
    number = bin(number)[2:]

    zero = len(number) % 8
    if zero != 0:
        number = "0" * (8 - zero) + number

    text = ""
    for i in range(0, len(number), 8):
        text += chr(int(number[i:i+8], 2))
    return text

if __name__ == "__main__":
    alice = Import_key("Alice")
    bob = Import_key("Bob")

    print("Alice -> Bob")
    mess_number_0 = txt2int("Hello Bob")
    #mess_number_0 = random.randint(100000, 1000000)
    print("Open mess:", hex(mess_number_0)[2:])
    C_alice2bob = Encrypt(mess_number_0, alice.o_e, alice.o_n)
    print("Encrypted mess:", hex(C_alice2bob)[2:])

    M_alice2bob = Decrypt(C_alice2bob, bob.d, bob.n)
    print("Decrypted mess:", hex(M_alice2bob)[2:])
    print("Text:", int2txt(M_alice2bob))

    print("\nBob -> Alice")
    mess_number_1 = txt2int("Hello Alice")
    #mess_number_1 = random.randint(100000, 1000000)
    print("Open mess:", hex(mess_number_1)[2:])
    C_bob2alice = Encrypt(mess_number_1, bob.o_e, bob.o_n)
    print("Encrypted mess:", hex(C_bob2alice)[2:])
    
    M_bob2alice = Decrypt(C_bob2alice, alice.d, alice.n)
    print("Decrypted mess:", hex(M_bob2alice)[2:])
    print("Text:", int2txt(M_bob2alice))

    print("\nAlice -> Bob")
    S_from_alice = Sign(mess_number_0, alice.d, alice.n)
    print("S:", hex(S_from_alice)[2:])
    Bob_verify = Verify(S_from_alice, mess_number_0, bob.o_e, bob.o_n)
    print("Status:", Bob_verify)

    print("\nBob -> Alice")
    S_from_bob = Sign(mess_number_1, bob.d, bob.n)
    print("S:", hex(S_from_bob)[2:])
    Alice_verify = Verify(S_from_alice, mess_number_0, alice.o_e, alice.o_n) # <---
    print("Status:", Alice_verify)
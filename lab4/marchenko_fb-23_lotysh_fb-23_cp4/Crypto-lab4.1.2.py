#Marchenko Rodion RSA encryption/decryption program ver 1.0:

from congruencesolver import *

import sys
import time
import math, random

BOLD = "\033[1m"
END = "\033[0m"
YELLOW = "\033[0;33m"
BRED = "\033[1;31m"
BGREEN = "\033[1;32m"

def PrintHelp():
    print("""USAGE:
    -k --key         - Generate new set of two RSA keysets.
    -e --encrypt     - <text> <e> <n> - RSA encrypt.
    -d --decrypt     - <enc> <d> <n> - RSA decrypt.
    -s --sign        - <text> <d> <n> - Sign with RSA digital signature.
    -v --verify      - <text> <signed> <e> <n> - Verify RSA digital signature.
    -sk --sendkey    - <eB> <nB> <dA> <nA> - Send signed message for RSA key exchange.
    -rk --recievekey - <K1> <S1> <dB> <nB> <eA> <nA> - Recieve and process a
                        signed message for RSA key exchange.
    -h --help        - help.
        """)


### DATA PREPROCESSING FUNCTIONS:

#This function encodes a hex representation
# of an ASCII string as a single integral number.
def ASCIItextToNumber(InputText):
    TextBytes = InputText.encode(encoding="ascii")
    Encoded = int.from_bytes(TextBytes, byteorder='big')
    print("  Encrypted data bytes = " + str(hex(Encoded))[2:])
    return Encoded

#This function decodes an integral number to an ASCII string .
def NumberToASCIItext(InputNum):
    print("  Decrypted data bytes = " + str(hex(InputNum))[2:])
    StringLen = int((len(str(hex(InputNum))))/2) - 1
    if (len(str(hex(InputNum))) % 2 == 1):
        StringLen = StringLen + 1
    TextBytes = InputNum.to_bytes(StringLen, 'big')
    Decoded = TextBytes.decode(encoding="ascii")
    return Decoded



### RSA IMPLEMENTATION FUNCTIONS:

#This function raises a number to a given exponent by MOD N
# using the Horner method.
def HornerPow(base, exp, mod):
    lng = exp.bit_length()
    y = 1
    for i in reversed(range(lng)):
        y = (y * y) % mod
        if(not not(exp & (1 << i))):
            y = (y * base) % mod
    return y


#This function implements a prime number searching algorithm.
def MillerRabin(p):
    k = 16
    p1 = p - 1
    bits = format(p1, 'b')
    s = 0
    d = p1

    while(not(d & 1)):
        s += 1
        d = d >> 1

    for i in range(k):
        x = random.randrange(2, p - 1)
        gcd = ExtendedEuclidean(x, p)[1]
        if(gcd > 1):
            return False
        xr = HornerPow(x, d, p)
        if((xr == 1) or (xr == p1)):
            continue

        for r in range(1, s + 1):
            xr = HornerPow(xr, 2, p)
            if(xr == p1):
                break;
            elif(xr == 1):
                return False
            else:
                continue
        if(xr != p1):
            return False
    return True


#This function returns a random prime number.
def generatePrimeNumber(minlen, maxlen):
    while True:
        p = random.randrange(2**minlen, 2**(maxlen+1))
        if(not (p & 1)):
            continue
        if MillerRabin(p):
            return p
        else:
            continue


#This function generates a random new RSA keypair.
def GenerateKeyPair():
    p = generatePrimeNumber(256, 512)
    q = generatePrimeNumber(256, 512)
    n = p * q
    e = 65537 #2**16 + 1
    d = ExtendedEuclidean(e, (p-1)*(q-1))[0]
    return ((d, p, q), (e, n))


#This functions creates two key pairs for an RSA exchange,
# where p0q0 <= p1q1.
def GenerateKeyPairs():
    A = GenerateKeyPair()
    B = GenerateKeyPair()
    if((A[0][1]*A[0][2]) > (B[0][1]*B[0][2])):
        A, B = B, A
    return (A, B)



### RSA MAIN FUNCTIONS:

#This function encrypts data using the RSA algorithm.
def Encrypt(InputArray, e, n):
    EncryptedArray = []
    for i in range(0, len(InputArray)):
        Encrypted = HornerPow(InputArray[i], e, n)
        EncryptedArray.append(Encrypted)
    return EncryptedArray


#This function decrypts data, encrypted using the RSA algorithm.
def Decrypt(InputArray, d, n):
    DecryptedArray = []
    for i in range(0, len(InputArray)):
        Decrypted = HornerPow(InputArray[i], d, n)
        DecryptedArray.append(Decrypted)
    return DecryptedArray


#This function appends data with it`s owner's RSA digital signature.
def Sign(InputArray, d, n):
    SignedArray = []
    for i in range(0, len(InputArray)):
        Signed = HornerPow(InputArray[i], d, n)
        SignedArray.append([InputArray[i], Signed])
    return SignedArray


#This function verifies the RSA signature validity of number data
# using the owner's secret key.
def Verify(InputArray, e, n):
    verifiedArray = []
    for i in range(0, len(InputArray)):
        RecMsg = InputArray[i][0]
        S = InputArray[i][1]
        DecMsg = HornerPow(S, e, n)
        if (DecMsg != RecMsg):
            verifiedArray.append(False)
        else:
            verifiedArray.append(True)
    return verifiedArray


#This function creates a two part message for an RSA key exchange.
def SendKey(e2, n2, d1, n1, K=None):
    #(k2, S2) where k2 = (K**e2)mod n2; S2 = (S1**e2)mod n2; S1 = (K**d1)mod n1
    if (K == None):
        K = generatePrimeNumber(32, 64)

    S1 = Sign([K], d1, n1)
    K2 = Encrypt([K], e2, n2)
    S2 = Encrypt([S1[0][1]], e2, n2)
    return [K, K2[0], S2[0]]


#This function retrieves the secret from an RSA key exchange message
# and verifies it's validity.
def ReceiveKey(Msg, d2, n2, e1, n1):
    # retrieve k = (k2**d2)mod n2; S1 = (S2**d2)mod n2; verify k = (S1**e1)mod n1
    K2 = Msg[0]
    S2 = Msg[1]

    K = Decrypt([K2], d2, n2)
    S1 = Decrypt([S2], d2, n2)
    Ver = Verify([[K[0], S1[0]]], e1, n1)
    return [K[0], Ver[0]]



##### Driver code: #####
argc = len(sys.argv)

print(YELLOW+"""
╔════════════════════════════════════════════════════════════════╗
║ Custom RSA encryption-decryption & digital certificate program ║
╚════════════════════════════════════════════════════════════════╝
    """+END)


if (argc == 2 and ((sys.argv[1] == "-k") or (sys.argv[1] == "--key"))):
    A, B = GenerateKeyPairs()
    print(BOLD+" A:"+END)
    print("\tPublic Key  (e) = "+str(A[1][0])+"\n\tPrivate key (d) = "+str(A[0][0])+"\n\tModulus     (n) = "+str(A[1][1]))

    print(BOLD+"\n B:"+END)
    print("\tPublic Key  (e) = "+str(B[1][0])+"\n\tPrivate key (d) = "+str(B[0][0])+"\n\tModulus     (n) = "+str(B[1][1]))

elif (argc == 5):
    if((sys.argv[1] == "-e") or (sys.argv[1] == "--encrypt")):
        print(BOLD+"  RSA Encryption:"+END)
        try:
            Payload = ASCIItextToNumber(sys.argv[2])
            C = Encrypt([Payload], int(sys.argv[3]), int(sys.argv[4]))
            print("\n  Cyphertext     (C) = " + str(C[0]))
            print("  Cyphertext Hex (C) = " + str(hex(C[0]))[2:]+"\n")
        except:
            print(BRED+"\tERROR!"+END+" Cannot encode text data for encryption!")

    elif((sys.argv[1] == "-d") or (sys.argv[1] == "--decrypt")):
        print(BOLD+"  RSA Decryption:"+END)
        try:
            Payload = Decrypt([int(sys.argv[2])], int(sys.argv[3]), int(sys.argv[4]))
            M = NumberToASCIItext(Payload[0])
            print("\n  Cleantext (M) = " + str(M)+"\n")
        except:
            print(BRED+"\tERROR!"+END+" Cannot decode deciphered text data!")

    elif((sys.argv[1] == "-s") or (sys.argv[1] == "--sign")):
        print(BOLD+"  RSA Digital signature:"+END)
        try:
            Payload = ASCIItextToNumber(sys.argv[2])
            Signed = Encrypt([Payload], int(sys.argv[3]), int(sys.argv[4]))
            print("\n  Message       (M) = " + sys.argv[2])
            print("  Signature     (S) = " + str(Signed[0]))
            print("  Signature Hex (S) = " + str(hex(Signed[0]))[2:]+"\n")
        except:
            print(BRED+"\tERROR!"+END+" Cannot sign text data!")

    else:
       PrintHelp()

elif (argc == 6):
    if((sys.argv[1] == "-v") or (sys.argv[1] == "--verify")):
        print(BOLD+"  RSA Digital signature verification:"+END)
        try:
            Payload = ASCIItextToNumber(sys.argv[2])
            Ver = Verify([[Payload, int(sys.argv[3])]], int(sys.argv[4]), int(sys.argv[5]))
            if (Ver[0] == True):
                print("\n  Verification == "+BGREEN+"TRUE\n"+END)
            else:
                print("\n  Verification == "+BRED+"FALSE\n"+END)
        except:
            print(BRED+"\tERROR!"+END+" Cannot verify signed text data!")

    elif((sys.argv[1] == "-sk") or (sys.argv[1] == "--sendkey")):
        print(BOLD+"  RSA Key exchange send data:"+END)
        try:
            K, K2, S = SendKey(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), K=None)
            print("\n  Secret     (K) = " + str(K))
            print("  Key       (K1) = " + str(K2))
            print("  Signature (S1) = " + str(S)+"\n")

        except:
            print(BRED+"\tERROR!"+END+" Cannot create RSA key exchange message!")

    else:
       PrintHelp()

elif(argc == 8 and ((sys.argv[1] == "-rk") or (sys.argv[1] == "--recievekey"))):
    print(BOLD+"  RSA Key exchange recieve data:"+END)
    try:
        K, Ver = ReceiveKey([int(sys.argv[2]), int(sys.argv[3])], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
        print("\n  Key decrypted (K) = " + str(K))
        if (Ver == True):
            print("  Verification == "+BGREEN+"TRUE\n"+END)
        else:
            print("  Verification == "+BRED+"FALSE\n"+END)

    except:
        print(BRED+"\tERROR!"+END+" Cannot decode recieved RSA key exchange pair!")

else:
    PrintHelp()






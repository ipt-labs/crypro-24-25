from affine_cipher import inverse
from primes import oyler_phi, select_primes_pair, select_two_primes_pairs, swift_power


E_STANDARD = 2 ** 16 + 1
KEY_STORE_PATH = ".\\"


def generate_key_pair(p=None, q=None, n0=2 ** 256, n1=2 ** 257):
    if p is None or q is None:
        p, q = select_primes_pair(n0, n1)
    n = p * q
    e = E_STANDARD
    while True:
        d = inverse(e, oyler_phi(p, q))
        if d is not None:
            break

        e = e * 2 + 1
    return d, e, n


def encrypt(message, e, n):
    encrypted = swift_power(message, e, n)
    return encrypted


def decrypt(encrypted, d, n):
    message = swift_power(encrypted, d, n)
    return message


def sign(message, d, n):
    signature = swift_power(message, d, n)
    return message, signature


def verify(message, signature, e, n):
    m = swift_power(signature, e, n)
    return m == message


def send_key(k, e1, n1, d, n):
    k1 = swift_power(k, e1, n1)
    s = swift_power(k, d, n)
    s1 = swift_power(s, e1, n1)
    return k1, s1


def receive_key(k1, s1, e, n, d1, n1):
    k = swift_power(k1, d1, n1)
    s = swift_power(s1, d1, n1)
    kk = swift_power(s, e, n)
    return k if kk == k else None


def _make_hex_wo_0x(n):
    return hex(n)[2:]


class Caller:

    def __init__(self, name, p=None, q=None, keystore=KEY_STORE_PATH):
        self._name = name
        self._p = p
        self._q = q
        self._keystore = keystore
        if p is None or q is None:
            self._d = self._e = self._n = None
            return

        self._d, self._e, self._n = generate_key_pair(self._p, self._q)

    @property
    def name(self):
        return self._name

    @classmethod
    def from_files(cls, name, keystore=KEY_STORE_PATH, filename_pub="", fileanme_sec=""):
        caller = cls(name, keystore=keystore)
        caller.load_own_public_key(filename_pub)
        caller.load_own_secret_key(fileanme_sec)
        return caller

    def save_own_public_key(self, filename=""):
        if not filename:
            filename = f"{self._name}_pub.txt"
        with open(self._keystore + filename, 'w') as f:
            print(f"{_make_hex_wo_0x(self._n)}\n{_make_hex_wo_0x(self._e)}\n", file=f)

    def save_own_secret_key(self, filename=""):
        if not filename:
            filename = f"{self._name}_sec.txt"
        with open(self._keystore + filename, 'w') as f:
            print(f"{_make_hex_wo_0x(self._d)}", file=f)
            print(f"{_make_hex_wo_0x(self._p)}", file=f)
            print(f"{_make_hex_wo_0x(self._q)}", file=f)

    def load_own_public_key(self, filename=""):
        if not filename:
            filename = f"{self._name}_pub.txt"
        with open(self._keystore + filename, 'r') as f:
            self._n = int(f.readline(), 16)
            self._e = int(f.readline(), 16)

    def load_own_secret_key(self, filename=""):
        if not filename:
            filename = f"{self._name}_sec.txt"
        with open(self._keystore + filename, 'r') as f:
            self._d = int(f.readline(), 16)
            self._p = int(f.readline(), 16)
            self._q = int(f.readline(), 16)

    def save_public_key(self, filename, e, n):
        with open(self._keystore + filename, 'w') as f:
            print(f"{_make_hex_wo_0x(n)}\n{_make_hex_wo_0x(e)}\n", file=f)

    def load_public_key(self, filename):
        with open(self._keystore + filename, 'r') as f:
            n = int(f.readline(), 16)
            e = int(f.readline(), 16)
        return e, n

    def get_public_key(self):
        return self._e, self._n

    def encrypt(self, message, e, n):
        return encrypt(message, e, n)

    def decrypt(self, encrypted):
        return decrypt(encrypted, self._d, self._n)

    def sign(self, message):
        return sign(message, self._d, self._n)

    def verify(self, message, signature, e, n):
        return verify(message, signature, e, n)

    def send_key(self, k, e, n):
        return send_key(k, e, n, self._d, self._n)

    def receive_key(self, k1, s1, e, n):
        return receive_key(k1, s1, e, n, self._d, self._n)

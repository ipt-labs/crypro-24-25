from decimal import Decimal, getcontext
getcontext().prec = 50

import itertools

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def readText(fileName: str):
    with open(fileName, "r", encoding="utf-8") as f:
        return clear_text(f.read())

def clear_text(text: str) -> str:
    clear = ""
    for i in text.lower():
        if i not in ALPHABET:
            continue
        clear += i
    return clear

def gcdEuclideanExtended(a: int, m: int) -> tuple[int]:
    """
    Вираховує НСД(a, m) та повертає відповідні коефіцієнти u, v.
    gcd(a, m) = um + va.
    """
    if a == 0:
        return m, 0, 1
    
    # gcd(a, m) = um + va.
    gcd, u, v = gcdEuclideanExtended(m % a, a)
    return gcd, v - (m // a) * u, u

def gcdEuclideanExtended2(a: int, m: int) -> tuple[int]:
    """
    u(0) = 1, u(1) = 0, u(i+1) = u(i-1) - q(i) * u(i);
    """
    modulo = m
    a, m = abs(a), abs(m)
    if a == 0:
        return m, 0
    if m == 0:
        return a, 0
    
    u0, u1 = 1, 0
    while m:
        u0, u1 = u1, u0 - (a // m) * u1
        a, m = m, a % m

    return a, u0 % modulo

def modularInverse(a: int, m: int) -> tuple[int, bool]:
    """
    Повертає обернене a за модулем m. a**(-1) mod m.
    """
    gcd, v, _ = gcdEuclideanExtended(a, m)
    if gcd != 1:
        print(f"[!] ERROR: Variables a = {a} and m = {m} are not mutually prime!")
        return gcd, True
    
    # v = a**(-1) mod m.
    return v % m, False

def linearCongruence(a: int, b: int, m: int) -> tuple[list[int], bool]:
    """
    Повертає списком усі розв'язки лінійного порівняння ax = b mod m.
    """
    gcd, _, _ = gcdEuclideanExtended(a, m)
    if gcd == 1:
        return [(modularInverse(a, m)[0] * b) % m], False
    
    # Return error if b cannot be divided by gcd ≠ 1.
    if b / gcd != b // gcd:
        print(f"[!] ERROR: gcd(a = {a}, m = {m}) = {gcd} (≠ 1), but b = {b} cannot be divided by {gcd}!!")
        return [], True
    
    solutions: list[int] = []
    a //= gcd
    b //= gcd
    m //= gcd

    root = (modularInverse(a, m)[0] * b) % m
    solutions.append(root)
    
    for r in range(1, gcd):
        solutions.append(root + r*m)

    return solutions, False

def countDistinctBigrams(data: str) -> dict[int, int]:
    bigramCounts: dict[int, int] = {i: 0 for i in range(len(ALPHABET)**2)}

    for i in range(0, len(data), 2):
        bigramCounts[ALPHABET.index(data[i]) * len(ALPHABET) + ALPHABET.index(data[i + 1])] += 1

    return bigramCounts

def countBigrams(data: str) -> tuple[dict[str, int], int]:
    """
    Вираховує загальну кількість біграм, що не перетинаються,
    та кількість кожної з біграм.
    """
    totalBigramCount: int = 0
    bigramCounts: dict[str, int] = {c1 + c2: 0 for c1 in ALPHABET for c2 in ALPHABET}

    for i in range(len(data) // 2):
        bigramCounts[data[i*2:i*2+2]] += 1
        totalBigramCount += 1

    return bigramCounts, totalBigramCount

def calculateFrequencies(data: str) -> dict[str, Decimal]:
    """
    Вираховує частоту кожної біграми у тексті. Повертає найчастіші 5.
    """
    bigramCounts, totalBigramCount = countBigrams(data)
    return dict(itertools.islice(dict(sorted({bigram: Decimal(count) / Decimal(totalBigramCount) for bigram, count in bigramCounts.items()}.items(), key=lambda item: item[1], reverse=True)).items(), 5))

def calculateFrequenciesFirst(data: str, count: int) -> list[tuple[str, Decimal]]:
    bigramCounts, totalBigramCount = countBigrams(data)
    freqs: dict[str, Decimal] = {bigram: Decimal(count) / Decimal(totalBigramCount) for bigram, count in bigramCounts.items()}
    return sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:count]

def bigramToNumber(s: str) -> int:
    if len(s) != 2:
        raise Exception("len of string must be equal 2")
    
    return ALPHABET.index(s[0])*len(ALPHABET) + ALPHABET.index(s[1])

def numberToBigram(n: int) -> str:
    return ALPHABET[n//len(ALPHABET)] + ALPHABET[n%len(ALPHABET)]

class AfineDecryptor:
    a: int
    aInv: int
    b: int
    m: int
    valid: bool

    def __init__(self, a, b, m):
        self.a = a

        gcd, aInv = gcdEuclideanExtended2(a, m)
        if gcd != 1:
            self.valid = False
            print(f"a doesn't have a^(-1), gcd = {gcd}")
            return
        self.valid = True
        self.aInv = aInv
        self.b = b
        self.m = m

    def encrypt(self, s: str) -> str:
        if not self.valid or len(s)%2 == 1:
            return ""
        
        enc = ""
        # y = a*x + b mod m
        for i in range(0, len(s), 2):
            x = bigramToNumber(s[i:i+2])
            y = (self.a * x + self.b) % self.m
            enc += numberToBigram(y)

        return enc


    def decrypt(self, s: str) -> str:
        if not self.valid or len(s)%2 == 1:
            return ""
        
        dec = ""
        # x = (y-b)*(a**(-1)) mod m
        for i in range(0, len(s), 2):
            y = bigramToNumber(s[i:i+2])
            x = ((y-self.b)*self.aInv) % self.m
            dec += numberToBigram(x)
        
        return dec

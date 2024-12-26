from collections import Counter
import math

class VigenereCipher:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.m = len(alphabet)

    def clean_text(self, text):
        text = text.lower().replace('ё', 'е')
        return ''.join(ch for ch in text if ch in self.alphabet)

    def to_numbers(self, text):
        return [self.alphabet.index(ch) for ch in text]

    def from_numbers(self, nums):
        return ''.join(self.alphabet[i] for i in nums)

    def decrypt(self, ciphertext_nums, key_nums):
        return [ (c - key_nums[i % len(key_nums)]) % self.m 
                 for i, c in enumerate(ciphertext_nums) ]

class TextAnalysis:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.m = len(alphabet)
        self.freq_rus = {
            'о': 0.1097, 'е': 0.0845, 'а': 0.0801, 'и': 0.0735, 'н': 0.0670,
            'т': 0.0626, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0440,
            'к': 0.0349, 'м': 0.0321, 'д': 0.0298, 'п': 0.0281, 'у': 0.0262,
            'я': 0.0200, 'ы': 0.0186, 'ь': 0.0174, 'г': 0.0169, 'з': 0.0165,
            'б': 0.0145, 'ч': 0.0123, 'й': 0.0104, 'х': 0.0097, 'ж': 0.0094,
            'ш': 0.0073, 'ю': 0.0064, 'ц': 0.0048, 'щ': 0.0036, 'э': 0.0031,
            'ф': 0.0013, 'ъ': 0.0004
        }

    def coincidence_index(self, text):
        # повертаємо середнє значення (I)
        n = len(text)
        if n < 2: 
            return 0.0
        counts = Counter(text)
        s = sum(v * (v - 1) for v in counts.values())
        return s / (n*(n-1))

    def coincidence_statistics(self, text, r):
        #Рахуємо D(r)
        d = 0
        for i in range(len(text) - r):
            if text[i] == text[i + r]:
                d += 1
        return d

    def chi_squared(self, block_nums, shift):
        # Розшифруємо блок як шифр Цезаря (зсув shift)
        dec_nums = [ (bn - shift) % self.m for bn in block_nums ]
        dec_str = ''.join(self.alphabet[num] for num in dec_nums)
        
        counts = Counter(dec_str)
        n = len(dec_str)
        if n == 0: 
            return float('inf')

        chi2 = 0.0
        for letter in self.alphabet:
            observed = counts[letter]
            expected = self.freq_rus.get(letter, 0) * n
            chi2 += (observed - expected)**2 / (expected + 1e-12)  # щоб не ділити на 0

        return chi2

def find_best_period(text, alph):
    analysis = TextAnalysis(alph)

    best_r_D = 0
    best_Dval = 0

    best_r_I = 0
    best_Ival = 0.0

    # зберігатимемо також проміжні, щоб проаналізувати потім
    D_list = {}
    I_list = {}

    for r in range(2, 31):
        d_val = analysis.coincidence_statistics(text, r)
        D_list[r] = d_val
        if d_val > best_Dval:
            best_Dval = d_val
            best_r_D = r

        # середнє I для блоків
        block_indexes = []
        for start in range(r):
            block = text[start::r]
            block_indexes.append(analysis.coincidence_index(block))
        avg_i = sum(block_indexes)/len(block_indexes)
        I_list[r] = avg_i
        if avg_i > best_Ival:
            best_Ival = avg_i
            best_r_I = r

    # формуємо список кандидатів
    candidates = {best_r_D, best_r_I}  # щоб не було дублів, якщо співпали
    return list(candidates)

def find_key_for_period(ciphertext_nums, r, alph):
    """
    Знаходимо ключ довжини r методом мінімуму χ2.
    Пробуємо для кожного блоку знайти такий зсув, 
    щоб частоти розшифрованого блоку були найближчі до еталонних.
    """
    analysis = TextAnalysis(alph)
    key_nums = []
    for start in range(r):
        block_nums = ciphertext_nums[start::r]
        # шукаємо shift, який мінімізує chi2
        best_shift = 0
        best_chi2 = float('inf')
        for possible_shift in range(analysis.m):
            c2 = analysis.chi_squared(block_nums, possible_shift)
            if c2 < best_chi2:
                best_chi2 = c2
                best_shift = possible_shift
        key_nums.append(best_shift)
    return key_nums

def main():
    alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    cipher = VigenereCipher(alph)

    with open('cipher.txt', 'r', encoding='utf-8') as f:
        ciphertext_raw = f.read()

    ciphertext_cleaned = cipher.clean_text(ciphertext_raw)
    ciphertext_nums = cipher.to_numbers(ciphertext_cleaned)

    # 1. Знаходимо кандидатів на період
    r_candidates = find_best_period(ciphertext_cleaned, alph)
    print("Кандидати на період:", r_candidates)

    # 2. Для кожного кандидата шукаємо ключ через мінімум χ2
    for r in r_candidates:
        key_nums = find_key_for_period(ciphertext_nums, r, alph)
        key_str = cipher.from_numbers(key_nums)

        # 3. Спробуємо розшифрувати
        decrypted_nums = cipher.decrypt(ciphertext_nums, key_nums)
        decrypted_text = cipher.from_numbers(decrypted_nums)

        print(f"\n--- Період r = {r} ---")
        print(f"Знайдений ключ: {key_str}")
        with open('opentext.txt', 'w', encoding='utf-8') as out_f:
            out_f.write(decrypted_text)
        print("Дешифрований текст записано у файл opentext.txt")

if __name__ == '__main__':
    main()

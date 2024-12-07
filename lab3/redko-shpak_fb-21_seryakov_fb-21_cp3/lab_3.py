from flask import Flask, render_template, request, jsonify
from collections import Counter
import itertools

def extended_gcd(a, b):
    """ Розширений алгоритм Евкліда. """
    u = [1, 0]
    v = [0, 1]
    r = [a, b]
    
    i = 1
    while r[i] != 0:
        q = r[i-1] // r[i]
        r.append(r[i-1] - q * r[i])
        u.append(u[i-1] - q * u[i])
        v.append(v[i-1] - q * v[i])
        i += 1

    return r[i-1], u[i-1], v[i-1]

def mod_inverse(a, m):
    """ Знаходить мультиплікативний обернений елемент a^1 mod m. """
    d, u, v = extended_gcd(a, m)

    if d != 1:
        return None
    
    return u % m

def solve_linear_congruence(a, b, n):
    """ Розв'язує лінійне порівняння ax == b (mod n). """
    d, u, v = extended_gcd(a, n)
    
    if b % d != 0:
        return []
    
    if d > 1:
        a_1 = a // d
        b_1 = b // d
        n_1 = n // d
        a_1_inv = mod_inverse(a_1, n_1)
        x_0 = (a_1_inv * b_1) % n_1

        return [(x_0 + i * n_1) % n for i in range(d)]

    a_inv = mod_inverse(a, n)
    return [(a_inv * b) % n]

class TextProcessor:
    def __init__(self):
        # розмір алфавіту (рос. мова без ё, з заміною ъ на ь)
        self.m = 31
        self.m_squared = self.m * self.m
        
        self.alpha = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
        self.char_to_num = {char: num for num, char in enumerate(self.alpha)}
        self.num_to_char = {num: char for num, char in enumerate(self.alpha)}
        
        # найчастіші біграми рос. мови (з методички)
        self.common_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    
    def filter_text(self, text):
        text = text.lower()
        text = text.replace('ё', 'е').replace('ъ', 'ь')
        return ''.join(char for char in text if char in self.char_to_num)
    
    def text_to_numbers(self, text):
        """ текст у послідовність чисел (індексів букв) """
        return [self.char_to_num[char] for char in text]
    
    def numbers_to_text(self, numbers):
        """ послідовність чисел назад у текст """
        return ''.join(self.num_to_char[num % self.m] for num in numbers)
    
    def get_bigram_number(self, bigram):
        """ біграму в число X = x_1m + x_ """
        x1, x2 = bigram
        return (x1 * self.m + x2) % self.m_squared
    
    def get_number_bigram(self, number):
        """ число назад у біграму (x_1, x_2) """
        x1 = number // self.m
        x2 = number % self.m
        return (x1, x2)

    def get_text_bigrams(self, text, overlapping=False):
        """ розбиває текст на біграми """
        if overlapping:
            return [text[i:i+2] for i in range(len(text)-1)]
        return [text[i:i+2] for i in range(0, len(text)-1, 2)]
    
    def analyze_bigrams(self, text, n=5, overlapping=False):
        """ знаходить n найчастіших біграм у тексті """
        # фільтруємо текст та отримуємо біграми
        text = self.filter_text(text)
        bigrams = self.get_text_bigrams(text, overlapping)
        
        # рахуємо та нормалізуємо частоти
        bigram_freq = Counter(bigrams)
        total_bigrams = sum(bigram_freq.values())
        frequencies = {bigram: count / total_bigrams for bigram, count in bigram_freq.items()}
        
        # повертаємо найчастіші біграми
        return sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_bigram_pairs(self, encrypted_freq_bigrams):
        """ створює пари (X*, Y*) для аналізу на основі частих біграм """
        pairs = []
        
        # часті біграми мови в числа
        known_numbers = [self.get_bigram_number(
            (self.char_to_num[b[0]], self.char_to_num[b[1]]))
            for b in self.common_bigrams
        ]
        
        # часті біграми шифротексту в числа
        encrypted_numbers = [self.get_bigram_number(
            (self.char_to_num[b[0]], self.char_to_num[b[1]]))
            for b in encrypted_freq_bigrams
        ]
        
        # всі можливі пари для аналізу
        for x in known_numbers:
            for y in encrypted_numbers:
                pairs.append((x, y))
        
        return pairs

class AffineCryptanalysis:
    def __init__(self, m=31):
        self.m = m
        self.m_squared = m * m
        
    def encrypt_bigram(self, X, a, b):
        """ шифрує біграми за формулою Y = (aX + b) mod m^2 """
        return (a * X + b) % self.m_squared
    
    def decrypt_bigram(self, Y, a, b):
        """ дешифрує біграми за формулою X = a^(-1)(Y - b) mod m^2 """
        a_inv = mod_inverse(a, self.m_squared)
        if a_inv is None:
            raise ValueError(f"Не існує оберненого до {a} за модулем {self.m_squared}")
        return (a_inv * (Y - b)) % self.m_squared
    
    def find_possible_keys(self, x1, y1, x2, y2):
        """ знаходить можливі ключі (a,b) за двома парами біграм (X*, Y*) і (X**, Y**) """
        diff_y = (y1 - y2) % self.m_squared
        diff_x = (x1 - x2) % self.m_squared
        
        possible_a = solve_linear_congruence(diff_x, diff_y, self.m_squared)
        
        keys = []
        for a in possible_a:
            if mod_inverse(a, self.m_squared) is not None:
                b = (y1 - a * x1) % self.m_squared
                keys.append((a, b))
        
        return keys
    
    def encrypt_text(self, text_numbers, a, b):
        """ шифрує послідовності чисел (які відповідають біграмам тексту) """
        encrypted = []
        for i in range(0, len(text_numbers), 2):
            X = (text_numbers[i] * self.m + text_numbers[i + 1]) % self.m_squared
            Y = self.encrypt_bigram(X, a, b)
            encrypted.extend([Y // self.m, Y % self.m])
        return encrypted
    
    def decrypt_text(self, text_numbers, a, b):
        """ дешифрує послідовності чисел (які відповідають біграмам тексту) """
        decrypted = []
        for i in range(0, len(text_numbers), 2):
            Y = (text_numbers[i] * self.m + text_numbers[i + 1]) % self.m_squared
            X = self.decrypt_bigram(Y, a, b)
            decrypted.extend([X // self.m, X % self.m])
        return decrypted

class LanguageDetector:
    def __init__(self):
        # частоти рос. мови
        self.common_letters = {'о': 0.10983, 'е': 0.08483, 'а': 0.07998}
        self.rare_letters = {'ф': 0.00267, 'щ': 0.00361, 'ь': 0.01735}
        self.common_bigrams = {'ст': 0.0216, 'но': 0.0169, 'то': 0.0168, 'на': 0.0167, 'ен': 0.0159}
        
        # заборонені біграми (ніколи не зустрічаються в рос мові)
        self.forbidden_bigrams = {
            'ьь', 'ыь', 'щщ', 'щч', 'щй', 'щц', 'щш', 'щщ', 'щэ', 'щю', 'щя',
            'ьы', 'ьэ', 'ыы', 'ыэ', 'эы', 'эь', 'юы', 'юь', 'яы', 'яь'
        }
        
        # порогові значення для різних критеріїв
        self.letter_freq_threshold = 0.4  # допустиме відхилення для частот літер
        self.rare_letter_threshold = 0.05  # макс сумарна частота рідких літер
        self.forbidden_threshold = 0.01    # макс частота заборонених біграм
        self.bigram_threshold = 0.3        # мін схожість біграмного профілю

    def calculate_letter_frequencies(self, text):
        """ обчислює частоти літер у тексті """
        counter = Counter(text)
        total = len(text)
        return {char: count/total for char, count in counter.items()}

    def calculate_bigram_frequencies(self, text):
        """ обчислює частоти біграм на перетині """
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
        counter = Counter(bigrams)
        total = len(bigrams)
        return {bigram: count/total for bigram, count in counter.items()}

    def check_common_letters(self, frequencies):
        """ перевіряє частоти частих літер """
        error = 0
        for letter, expected_freq in self.common_letters.items():
            actual_freq = frequencies.get(letter, 0)
            error += abs(actual_freq - expected_freq) / expected_freq
        return error/len(self.common_letters) <= self.letter_freq_threshold

    def check_rare_letters(self, frequencies):
        """ перевіряє частоти рідких літер """
        total_rare = sum(frequencies.get(letter, 0) for letter in self.rare_letters)
        return total_rare <= self.rare_letter_threshold

    def check_forbidden_bigrams(self, text):
        """ перевіряє наявність заборонених біграм """
        bigram_freqs = self.calculate_bigram_frequencies(text)
        forbidden_freq = sum(bigram_freqs.get(bigram, 0) for bigram in self.forbidden_bigrams)
        return forbidden_freq <= self.forbidden_threshold

    def check_common_bigrams(self, text):
        """ перевіряє частоти найбільш поширених біграм """
        bigram_freqs = self.calculate_bigram_frequencies(text)
        matches = 0
        for bigram in self.common_bigrams:
            if bigram in bigram_freqs:
                actual_freq = bigram_freqs[bigram]
                expected_freq = self.common_bigrams[bigram]
                if abs(actual_freq - expected_freq) / expected_freq <= 0.5:
                    matches += 1
        return matches >= len(self.common_bigrams) * self.bigram_threshold

    def is_meaningful_text(self, text):
        """ перевірка осмисленості тексту"""
        text = text.lower()
        text = text.replace('ё', 'е').replace('ъ', 'ь')
        text = ''.join(c for c in text if c.isalpha())
        
        if len(text) < 100:
            return False
            
        frequencies = self.calculate_letter_frequencies(text)
        
        # всі критерії
        criteria = [
            self.check_common_letters(frequencies),
            self.check_rare_letters(frequencies),
            self.check_forbidden_bigrams(text),
            self.check_common_bigrams(text)
        ]
        
        # якщо проходить більшість критеріїв => вважається осмисленим
        return sum(criteria) >= 3

class CryptanalysisSystem:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.cryptanalysis = AffineCryptanalysis()
        self.language_detector = LanguageDetector()
        self.logs = []
        
    def log(self, message):
        self.logs.append(message)
        print(message)
        
    def analyze_ciphertext(self, ciphertext):
        self.logs = []
        self.log("[x] Початок аналізу шифротексту...")

        # 1. попередня обробка тексту
        filtered_text = self.text_processor.filter_text(ciphertext)
        text_numbers = self.text_processor.text_to_numbers(filtered_text)
        
        # 2. знаходження 5 найчастіших біграм
        frequent_bigrams = [pair[0] for pair in self.text_processor.analyze_bigrams(filtered_text, n=5)]
        self.log(f"[+] Найчастіші біграми шифротексту: {frequent_bigrams}")
        
        # 3. генерація всіх можливих пар біграм для аналізу
        bigram_pairs = self.text_processor.get_bigram_pairs(frequent_bigrams)
        
        # 4. перебір пар біграм та пошук можливих ключів
        used_keys = set()
        best_result = None
        best_score = 0
        attempt_count = 0
        
        self.log("[x] Починаємо перебір пар біграм та пошук можливих ключів...")
        for (x1, y1), (x2, y2) in itertools.combinations(bigram_pairs, 2):
            possible_keys = self.cryptanalysis.find_possible_keys(x1, y1, x2, y2)
            
            for key in possible_keys:
                if key in used_keys:
                    continue
                used_keys.add(key)
                attempt_count += 1
                
                try:
                    decrypted_numbers = self.cryptanalysis.decrypt_text(text_numbers, key[0], key[1])
                    decrypted_text = self.text_processor.numbers_to_text(decrypted_numbers)
                    
                    if self.language_detector.is_meaningful_text(decrypted_text):
                        frequencies = self.language_detector.calculate_letter_frequencies(decrypted_text)
                        score = sum(1 for letter in self.language_detector.common_letters 
                                    if abs(frequencies.get(letter, 0) - 
                                        self.language_detector.common_letters[letter]) < 0.02)
                        
                        if score == 0:
                            continue
                        
                        self.log(f"[+] Спроба {attempt_count}: Ключ {key} - Текст: {decrypted_text[:100]}")
                        
                        if score > best_score:
                            best_score = score
                            best_result = (decrypted_text, key)
                            
                except Exception as e:
                    self.log(f"[×] Спроба {attempt_count}: Помилка дешифрування для ключа {key}: {e}")
                    continue
        
        if best_result is None:
            raise ValueError("[×] Не вдалося знайти правильний ключ")
        
        self.log(f"\n[✓] Знайдено успішний розшифрований текст після {attempt_count} спроб.")
        return best_result, self.logs


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        encrypted_text = data.get('text', '')
        
        if not encrypted_text:
            return jsonify({'error': 'Текст не може бути порожнім'}), 400
            
        system = CryptanalysisSystem()
        (decrypted_text, key), logs = system.analyze_ciphertext(encrypted_text)
        
        return jsonify({
            'success': True,
            'decrypted_text': decrypted_text,
            'key': {'a': key[0], 'b': key[1]},
            'logs': logs
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
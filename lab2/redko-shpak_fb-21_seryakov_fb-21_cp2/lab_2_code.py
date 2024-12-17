import random
import pandas as pd
import seaborn as sns
from collections import Counter
from math import gcd
from functools import reduce
import matplotlib.pyplot as plt

class CryptoConstants:
    def __init__(self):
        self.alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        self.letter_frequencies = {
            'о': 0.1106464800, 'а': 0.0863823704, 'е': 0.0812994808, 'и': 0.0684,
            'т': 0.0602991214, 'л': 0.0525426988, 'с': 0.0506917913, 'р': 0.0474,
            'к': 0.0365767408, 'у': 0.0300542565, 'м': 0.0300107844, 'п': 0.0284,
            'г': 0.0191527960, 'я': 0.0190691959, 'з': 0.0177767374, 'ь': 0.0177,
            'ч': 0.0159024219, 'б': 0.0154860931, 'й': 0.0117224140, 'ж': 0.0090,
            'х': 0.0082279275, 'ю': 0.0052801859, 'щ': 0.0035379587, 'ц': 0.0033,
            'ф': 0.0021602281, 'ъ': 0.0003210246
        }

class TextProcessor:
    def __init__(self):
        self.constants = CryptoConstants()
        
    def read_text(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read().lower()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не знайдено")

    def generate_random_text(self, original_text, size, min_length=20, max_length=50):
        if not original_text:
            raise ValueError("Вхідний текст порожній")
            
        fragments = [
            original_text[i:i+length]
            for length in range(min_length, max_length + 1)
            for i in range(len(original_text) - length + 1)
        ]
        
        if not fragments:
            return ""
            
        num_fragments = size // min_length
        random_text = ''.join(random.choice(fragments) for _ in range(num_fragments))
        return random_text[:size]

    def generate_keys(self, lengths):
        return [''.join(random.choice(self.constants.alphabet)
                for _ in range(length)) for length in lengths]
    

class VigenereCipher:
    def __init__(self):
        self.constants = CryptoConstants()
        
    def calculate_ioc(self, text):
        n = len(text)
        if n <= 1:
            return 0
        freqs = Counter(text)
        ioc = sum(count * (count - 1) for count in freqs.values()) / (n * (n - 1))
        return ioc

    def encrypt(self, plaintext, key):
        encrypted_text = []
        key_length = len(key)
        
        for i, char in enumerate(plaintext):
            if char in self.constants.alphabet:
                char_index = self.constants.alphabet.index(char)
                key_index = self.constants.alphabet.index(key[i % key_length])
                encrypted_text.append(self.constants.alphabet[
                    (char_index + key_index) % len(self.constants.alphabet)
                ])
            else:
                encrypted_text.append(char)
                
        return ''.join(encrypted_text)

    def decrypt(self, ciphertext, key):
        decrypted_text = []
        key_length = len(key)
        
        for i, char in enumerate(ciphertext):
            if char in self.constants.alphabet:
                char_index = self.constants.alphabet.index(char)
                key_index = self.constants.alphabet.index(key[i % key_length])
                decrypted_text.append(self.constants.alphabet[
                    (char_index - key_index) % len(self.constants.alphabet)
                ])
            else:
                decrypted_text.append(char)
                
        return ''.join(decrypted_text)

class CryptoAnalyzer:
    def __init__(self):
        self.constants = CryptoConstants()
        self.cipher = VigenereCipher()
        
    def count_frequencies(self, text):
        frequencies = Counter(text)
        total = sum(frequencies.values())
        return {char: freq / total for char, freq in frequencies.items()}

    def find_key_length(self, ciphertext, max_length=30):
        iocs = []
        
        for length in range(1, max_length + 1):
            ioc_sum = 0
            total_length = 0
            
            for i in range(length):
                substring = ciphertext[i::length]
                substring_length = len(substring)
                ioc_sum += self.cipher.calculate_ioc(substring) * substring_length
                total_length += substring_length
                
            avg_ioc = ioc_sum / total_length
            iocs.append((length, avg_ioc))
            
        iocs.sort(key=lambda x: x[1], reverse=True)
        
        plateau = [iocs[0]]
        for length, ioc in iocs[1:]:
            if ioc > iocs[0][1] * 0.9:
                plateau.append((length, ioc))
            else:
                break
                
        best_length = min(plateau, key=lambda x: x[0])
        
        print("\n[!] Топ-5 можливих довжин ключа [!]")
        for length, ioc in iocs[:5]:
            print(f" [+] Довжина {length}: IOC = {ioc:.6f}")
        print(f"\n[✓] Рекомендована довжина ключа: {best_length[0]}")
        
        return best_length[0], iocs


    def find_key(self, ciphertext, key_length):
        key = ''
        
        # проходимо по кожній колонці по довжині ключа
        for i in range(key_length): 
        
            column = ciphertext[i::key_length] # кожен key_length-ий символ

            freq = self.count_frequencies(column) # счітаєм частоти символів у колонці
            
            max_correlation = -1
            best_shift = 0
            
            # чекаєм всі можливі зсуви для алфавіту
            # лля кожного можливого зсуву (від 0 до лен алфавіта) чекаєм, наскільки добре цей зсув підходить.
            for shift in range(len(self.constants.alphabet)):
                correlation = 0
                
                # рахуємо кореляцію для кожного символу алфавіту (чим > тим краще і тим вирігдніший той зсув, шо ми найшли)
                for j in range(len(self.constants.alphabet)):
                    shifted_char = self.constants.alphabet[(j + shift) % len(self.constants.alphabet)]
                    original_char = self.constants.alphabet[j]
                    
                    # кореляція між частотою символу та частотою в алфавіті
                    correlation += freq.get(shifted_char, 0) * self.constants.letter_frequencies.get(original_char, 0)
                    
                # оновлюємо максимальне кореляційне значення та найкращий зсув, якщо потрібно
                if correlation > max_correlation:
                    max_correlation = correlation
                    best_shift = shift
                    
            key += self.constants.alphabet[best_shift]
            
        return key


class Visualizer:
    def __init__(self):
        self.analyzer = CryptoAnalyzer()
        
    def plot_ioc_comparison(self, ioc_plaintext, ioc_ciphertexts):
        plt.figure(figsize=(12, 6))
        data = {
            'Текст': ['Відкритий'] + [f'Шифр. {i+1}' for i in range(len(ioc_ciphertexts))],
            'IOC': [ioc_plaintext] + ioc_ciphertexts
        }
        
        sns.barplot(x='Текст', y='IOC', data=pd.DataFrame(data))
        plt.xlabel('Тексти')
        plt.ylabel('Індекс відповідності')
        plt.title('Порівняння індексів відповідності')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_frequency_distribution(self, text):
        freq = self.analyzer.count_frequencies(text)
        plt.figure(figsize=(15, 5))
        plt.bar(freq.keys(), freq.values())
        plt.title('Розподіл частот символів')
        plt.xlabel('Символи')
        plt.ylabel('Частота')
        plt.tight_layout()
        plt.show()
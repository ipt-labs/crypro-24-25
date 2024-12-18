russian_alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"

index_to_char_updated = {i: char for i, char in enumerate(russian_alphabet)}
char_to_index_updated = {char: i for i, char in enumerate(russian_alphabet)}

prohibited_bigrams = ['аь','аы','еь','еы','иь','иы','оь','оы','уь','уы','ьь','ьы','ыь','ыы','эь','эы','юь','юы','яь','яы','жы']
print(f"Список заборонених l-грам:\n {prohibited_bigrams}")

def calc_bigram_frequency(data, step_size=1):
    cleaned_data = ''.join(data)
    bigram_counts = {}
    for i in range(0, len(cleaned_data) - 1, step_size):
        bigram = cleaned_data[i:i + 2]
        bigram_counts[bigram] = bigram_counts.get(bigram, 0) + 1
    return bigram_counts


def display_bigram_frequency(bigram_frequencies):
    bigram_table = [(bigram, count, count / sum(bigram_frequencies.values())) for bigram, count in bigram_frequencies.items()]
    bigram_table.sort(key=lambda x: x[1], reverse=True)
    
    print("{:<10} {:<10} {:<10}".format("Символ", "Кількість", "Частота"))
    for bigram, count, frequency in bigram_table:
        print("{:<10} {:<10} {:<10.5f}".format(bigram, count, frequency))


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x, y = extended_gcd(b % a, a)
    x, y = y - (b // a) * x, x
    return gcd, x, y


def convert_bigrams_to_numbers(text):
    bigrams = [text[i:i + 2] for i in range(0, len(text), 2)]
    num_list = [char_to_index_updated[bigram[0]] * 31 + char_to_index_updated[bigram[1]] for bigram in bigrams]
    return num_list


def generate_bigram_combinations(set1, set2):
    combinations = []
    for item1 in set1:
        for item2 in set2:
            remaining_set1 = set1.copy()
            remaining_set2 = set2.copy()
            remaining_set1.remove(item1)
            remaining_set2.remove(item2)
            for item1_remaining in remaining_set1:
                for item2_remaining in remaining_set2:
                    combinations.append((item1, item2, item1_remaining, item2_remaining))
    return combinations


def find_keys_for_decryption(combinations):
    a_candidates, b_candidates = [], []
    for combo in combinations:
        x0, y0, x1, y1 = combo
        gcd, x, y = extended_gcd(31**2, x0 - x1)
        if gcd == 1:
            a = ((y0 - y1) * y) % 31**2
            b = (y0 - a * x0) % 31**2
            if a not in a_candidates:
                a_candidates.append(a)
                b_candidates.append(b)
        if gcd > 1:
            if (y0 - y1) % gcd == 0:
                a1 = (x0 - x1) // gcd
                b1 = (y0 - y1) // gcd
                n1 = 31**2 // gcd
                gcd1, _, y = extended_gcd(n1, a1)
                x = (b1 * y) % n1
                for i in range(gcd1):
                    a = x + i * n1
                    b = (y1 - a * x1) % 31**2
                    if a not in a_candidates:
                        a_candidates.append(a)
                        b_candidates.append(b)
    return a_candidates, b_candidates


def decrypt_text(a, b, cipher_text):
    numbers = convert_bigrams_to_numbers(cipher_text)
    decrypted_numbers = [(y * (num - b)) % 31**2 for num in numbers for _, _, y in [extended_gcd(31**2, a)]]
    return decrypted_numbers


def convert_numbers_to_bigrams(numbers):
    return [index_to_char_updated[num // 31] + index_to_char_updated[num % 31] for num in numbers]


def is_valid(decrypted_bigrams):
    return all(bigram not in prohibited_bigrams for bigram in decrypted_bigrams)


with open("10.txt", encoding="utf-8") as file:
    ciphertext = file.read()


display_bigram_frequency(bigram_frequencies=calc_bigram_frequency(ciphertext, 2))


a_candidates, b_candidates = find_keys_for_decryption(generate_bigram_combinations(set1=convert_bigrams_to_numbers('стнотонаен'), set2=convert_bigrams_to_numbers('сгжэямнгтм')))
print(f"\nМожливі значення ключа:\na:{a_candidates}\n\nb:{b_candidates}\n")


for i in range(len(a_candidates)):
    a_val, b_val = a_candidates[i], b_candidates[i]
    decrypted_numbers = decrypt_text(a_val, b_val, ciphertext)
    if is_valid(convert_numbers_to_bigrams(decrypted_numbers)):
        plaintext = ''.join(convert_numbers_to_bigrams(decrypted_numbers))
        print(f"\nЗначення ключа:\na={a_val}\nb={b_val}\n\nРозшифрований текст:{plaintext}")
        with open("decrypted_10.txt", "w", encoding="utf-8") as output_file:
            output_file.write(plaintext)
        break

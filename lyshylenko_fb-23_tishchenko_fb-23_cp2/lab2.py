alphabet='абвгдежзийклмнопрстуфхцчшщъыьэюя'
m=len(alphabet)

def read_file(filename):
    with open(filename, mode='r', encoding="utf8") as file:
        return file.read()

var7 = read_file('var7.txt')
levtolstoy = read_file('levtolstoy.txt')

def encrypt(text, key):
    key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]
    
    encrypted_text = ''.join(
        alphabet[(alphabet.index(char) + alphabet.index(key_char)) % m]    # Перевірка, чи символ входить до алфавіту
        if char in alphabet else char
        for char, key_char in zip(text, key_repeated)
    )
    
    return encrypted_text

keys = (                                                                         # Список ключів  
    'ок', 'нет', 'шифр', 'слова', 'шифрование', 'образование',
    'криптография', 'идентификация', 'робочийноутбук', 'относительность',
    'вариантномерсемь', 'ключшифравиженера', 'конфиденциальность',
    'левтолстойвойнаимир', 'лабораторнаяномердва'
)

with open('ciphers.txt', mode='w', encoding='utf8') as output_file:               # Відкриття файлу для запису результатів
    for key in keys:                                                             # Шифрування тексту з використанням ключів
        encrypted_text = encrypt(levtolstoy, key)
        output_file.write(f'Шифротекст з ключем "{key}":\n{encrypted_text}\n\n')

def calc_index(data):                                                             # Функція для обчислення індексу відповідності
    counts = [data.count(alphabet[x]) for x in range(m)]                          # Отримуємо список кількостей кожної букви
    index = sum(count * (count - 1) for count in counts)                          # Обчислюємо індекс відповідності
    index *= 1 / (len(data) * (len(data) - 1))
    return index

print("Індекс відповідності для відкритого тексту: ",calc_index(levtolstoy))

def indexes(block_size, data):         
    blocks = [data[i::block_size] for i in range(block_size)]          # Розбиття тексту на блоки
    index = sum(calc_index(block) for block in blocks) / len(blocks)   # Обчислення ІВ для кожного блоку
    return index

with open('indexes.txt', mode='w', encoding='utf8') as indexes_file:
    for key in keys:
        encrypted = encrypt(levtolstoy, key)
        value = calc_index(encrypted)
        indexes_file.write(f"{value} - індекс відповідності з ключем '{key}'\n")

with open('ІВ.txt', mode='w', encoding="utf8") as result_file:
    for block_size in range(1, m):   
        result = indexes(block_size, var7)
        #print(block_size, " - ", result)
        result_file.write(f"{block_size} - {result}\n")

letter = 'о'                                                                                        #найвживаніша літера в рос алфавіті.

def find_key(cipher_text, common_letters, key_length):                                              # функція для пошуку ключа
    text_segments = [cipher_text[i::key_length] for i in range(key_length)]                         # Розбиття тексту на сегменти

    key = ''.join(
        alphabet[(alphabet.index(max(segment, key=segment.count)) - alphabet.index(letter)) % m]
        for segment in text_segments                                                                # знайти найчастіший символ і зсув
    )
    return key

print("\nЗнайдений ключ:", find_key(var7, letter, 15))

correct_key='арудазовархимаг'                                                         #змістовний ключ

def decrypt(key, data):                                                               # Функція розшифрування
    decrypted_text = ''.join(
        alphabet[(alphabet.index(char) - alphabet.index(key[i % len(key)])) % m]
        for i, char in enumerate(data)
    )
    return decrypted_text

text = (decrypt(correct_key, var7))                                                   #розкодований текст
print("\nРозшифрований текст:")
print(text)

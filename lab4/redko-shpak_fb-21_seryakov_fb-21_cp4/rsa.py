import random
import logging
from typing import List, Union, Tuple, NamedTuple

# константи та формат логів
DEFAULT_E = 65537  # 2^16 + 1
MIN_BIT_LENGTH = 256
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
LOG_FORMATS = {
    'STEP': '[>]',      # кроки алгоритму і тд.
    'GENERATE': '[x]',  # генерація чогось
    'ENCRYPT': '[+]',   # шифрування
    'DECRYPT': '[-]',   # розшифрування
    'VERIFY': '[v]',    # перевірка (підпису, валідності і тд.)
    'ERROR': '[!]',     # помилки
    'INFO': '[i]',      # загальна інформація
    'SUCCESS': '[=]'    # успіх
}

# клас логів
class CustomFormatter(logging.Formatter):
    """ клас для форматування логів"""
    
    def format(self, record):
        msg_lower = record.msg.lower()
        
        if any(word in msg_lower for word in ["генерація", "generating", "згенеровано"]):
            prefix = LOG_FORMATS['GENERATE']
        elif any(word in msg_lower for word in ["крок", "step", "обчислення", "підготовка"]):
            prefix = LOG_FORMATS['STEP']
        elif any(word in msg_lower for word in ["розшифрування", "decrypt"]):
            prefix = LOG_FORMATS['DECRYPT']
        elif any(word in msg_lower for word in ["шифрування", "encrypt"]):
            prefix = LOG_FORMATS['ENCRYPT']
        elif any(word in msg_lower for word in ["перевірка", "валідація", "verify", "validation"]):
            prefix = LOG_FORMATS['VERIFY']
        elif record.levelno == logging.ERROR or "помилка" in msg_lower or "error" in msg_lower:
            prefix = LOG_FORMATS['ERROR']
        elif any(word in msg_lower for word in ["успішно", "success", "готово", "виконано"]):
            prefix = LOG_FORMATS['SUCCESS']
        else:
            prefix = LOG_FORMATS['INFO']
        
        return f"{prefix} {record.msg}"

def setup_logging():
    """ сетап для всьго проєкту """
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger = logging.getLogger()
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)

setup_logging()

# типи ключів для RSA
class RSAPublicKey(NamedTuple):
    e: int  # відкрита експонента
    n: int  # модуль

class RSAPrivateKey(NamedTuple):
    d: int  # секретна експонента
    p: int  # перше просте число
    q: int  # друге просте число
    n: int  # модуль (для зручності)

# математичні ф-ії
def gcd(a: int, b: int) -> int:
    """ найбільший спільний дільник """
    logging.debug(f"Обчислення НСД для чисел {a} та {b}")
    while b:
        a, b = b, a % b
    logging.debug(f"Результат НСД: {a}")
    return a

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """ розширений алгоритм Евкліда. повертає (gcd, x, y) такі, що a * x + b * y = gcd """
    logging.debug(f"Обчислення розширеного НСД для чисел {a} та {b}")
    
    if a == 0:
        return b, 0, 1
    
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
        logging.debug(f"Крок: частка={quotient}, r={r}, s={s}, t={t}")
    
    logging.debug(f"НСД = {old_r}, x = {old_s}, y = {old_t}")
    return old_r, old_s, old_t

def mod_inverse(a: int, m: int) -> int:
    """ знаходження мультиплікативного оберненого за модулем m. a * x ≡ 1 (mod m) """
    logging.info(f"Обчислення мультиплікативного оберненого для {a} за модулем {m}")
    
    if m == 1:
        return 0
    
    gcd_val, x, _ = extended_gcd(a, m)
    
    if gcd_val != 1:
        raise ValueError(f"Мультиплікативне обернене не існує (НСД({a}, {m}) ≠ 1)")
    
    result = x % m
    logging.info(f"Результат обчислення мультиплікативного оберненого: {result}")
    return result

def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """ Модульне піднесення до степеня (юзається схема Горнера base^exponent mod modulus) """
    logging.debug(f"Обчислення {base}^{exponent} mod {modulus}")
    
    if modulus == 1:
        return 0
    
    if exponent == 0:
        return 1
    
    binary_exp = bin(exponent)[2:]
    result = 1
    
    for bit in binary_exp:
        result = (result * result) % modulus
        if bit == '1':
            result = (result * base) % modulus
    
    return result

def bit_length(n: int) -> int:
    """ повертає довжину числа в бітах """
    return len(bin(n)) - 2

# генерація та перевірка простих чисел
def decompose_number(n: int) -> Tuple[int, int]:
    """ розкладає n-1 на добуток (2^s)*d, де d - непарне. повертає (s, d) """
    s = 0
    d = n - 1
    
    while d % 2 == 0:
        s += 1
        d //= 2
    
    return s, d

def trial_division(n: int) -> bool:
    """ тест пробних ділень на малі прості числа """
    if n < 2:
        return False
    if n in SMALL_PRIMES:
        return True
    if any(n % p == 0 for p in SMALL_PRIMES):
        return False
    
    return True

def miller_rabin_test(n: int, k: int = 40) -> bool:
    """ тест міллера-рабіна з k раундами """
    if n < 2:
        return False
    
    if not trial_division(n):
        return False
    
    s, d = decompose_number(n)
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = mod_pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(s - 1):
            x = mod_pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def generate_prime_candidate(bit_length: int) -> int:
    """ генерує рандомне непарне число заданої бітової довжини (не обов'язково просте) """
    n = random.getrandbits(bit_length)
    n |= (1 << bit_length - 1)
    n |= 1
    return n

def generate_prime(bit_length: int, k: int = 40) -> int:
    """ генерує рандомне  просте число заданої бітової довжини (точно просте) """
    while True:
        n = generate_prime_candidate(bit_length)
        if miller_rabin_test(n, k):
            return n

def generate_safe_prime(bit_length: int, k: int = 40) -> Tuple[int, int]:
    """ генерує безпечне просте число p таке, що q = (p-1)/2 також просте. повертає пару (p, q) """
    logging.info(f"Генерація {bit_length}-бітного безпечного простого числа...")
    
    while True:
        q = generate_prime(bit_length - 1, k)
        
        p = 2 * q + 1
        
        if miller_rabin_test(p, k):
            logging.info(f"Знайдено безпечне просте p = {p}")
            logging.info(f"Перевірка: q = (p-1)/2 = {q} - також просте число")
            logging.info(f"Перевірка: p = 2q + 1 = {p}")
            return p, q

# розбиття повідомлень на блоки, підготовки їх до RSA та відновлення оригінального повідомлення з блоків
class RSAMessage:
    """ клас для роботи з повідомленнями RSA """
    def __init__(self, content: Union[str, int], public_key: RSAPublicKey = None):
        self.is_text = isinstance(content, str)
        self.original_content = content
        self.blocks: List[int] = []
        self.original_bytes_length = 0
        
        if public_key:
            self.block_size = self.calculate_block_size(public_key.n)
            self._prepare_blocks(content, self.block_size)
    
    @staticmethod
    def calculate_block_size(n: int) -> int:
        # розмір блоку в байтах - це просто к-сть байт в n 1
        # (мінус 1 для гарантії, що блок буде менше n)
        return (n.bit_length() - 1) // 8

    @staticmethod
    def from_blocks(blocks: List[int], is_text: bool, block_size: int, original_bytes_length: int = 0) -> 'RSAMessage':
        """ створює повідомлення RSA з блоків """
        message = RSAMessage.__new__(RSAMessage)
        message.blocks = blocks
        message.is_text = is_text
        message.block_size = block_size
        message.original_bytes_length = original_bytes_length
        
        if is_text:
            message.original_content = message._blocks_to_text(blocks, block_size)
        else:
            message.original_content = message._blocks_to_number(blocks)
        
        return message

    def _prepare_blocks(self, content: Union[str, int], block_size: int):
        """ підготовка блоків залежно від типу вмісту (текст/число) """
        if self.is_text:
            self._prepare_text_blocks(content, block_size)
        else:
            self._prepare_number_blocks(content, block_size)
    
    def _prepare_text_blocks(self, text: str, block_size: int):
        """ розбиває текстове повідомлення на блоки (якщо велике) """
        logging.info(f"Підготовка текстового повідомлення: {len(text)} символів")
        bytes_data = text.encode('utf-8')
        
        for i in range(0, len(bytes_data), block_size):
            block = bytes_data[i:i + block_size]
            padded_block = block.ljust(block_size, b'\x00')
            number = int.from_bytes(padded_block, 'big')
            self.blocks.append(number)
            logging.debug(f"Блок  {i//block_size}: {len(block)} байт -> {number}")
        
        logging.info(f"Створено {len(self.blocks)} блоків")
    
    def _prepare_number_blocks(self, number: int, block_size: int):
        """ розділяє число на блоки відповідно до розміру модуля """
        max_block = (1 << (block_size * 8)) - 1  # макс значення блоку
        number_str = str(number)  # в рядок
        block_size_dec = len(str(max_block))  # розмір блоку в десяткових цифрах
        
        # розділяємо на блоки з кінця
        blocks = []
        while number_str:
            block = number_str[-block_size_dec:] if len(number_str) > block_size_dec else number_str
            number_str = number_str[:-block_size_dec] if len(number_str) > block_size_dec else ""
            blocks.insert(0, int(block))
        
        self.blocks = blocks
    
    def _blocks_to_number(self, blocks: List[int]) -> int:
        """ об'єднує блоки назад в число конкатенацією"""
        return int(''.join(str(block) for block in blocks))

    def _blocks_to_text(self, blocks: List[int], block_size: int) -> str:
        """ конвертує блоки назад у текст """
        text_parts = []
        
        for i, number in enumerate(blocks):
            try:
                block_bytes = number.to_bytes(block_size, 'big')
                if i == len(blocks) - 1:
                    block_bytes = block_bytes.rstrip(b'\x00')
                text_part = block_bytes.decode('utf-8')
                text_parts.append(text_part)
            except (ValueError, UnicodeDecodeError) as e:
                logging.error(f"Не вдалося декодувати блок {i}: {number}")
                raise ValueError(f"Не вдалося декодувати блок {i}: {str(e)}")
        
        result = ''.join(text_parts)
        logging.info(f"Успішно декодований текст: {len(result)} символів")
        return result

# генерація ключа
def validate_prime_pair(p: int, q: int, bit_length: int) -> bool:
    """ перевіряє пару простих чисел на відповність вимогам RSA """

    logging.debug(f"Перевірка пари простих чисел: p={p}, q={q}")
    
    # перевірка бітової довжини
    if p.bit_length() < bit_length or q.bit_length() < bit_length:
        logging.warning("Прості числа занадто малі")
        return False
    
    # перевірка простоти
    if not (miller_rabin_test(p) and miller_rabin_test(q)):
        logging.warning("Числа не є простими")
        return False
    
    # p і q повинні бути різними
    if p == q:
        logging.warning("Прості числа рівні")
        return False
    
    # перевірка, що p-1 і q-1 мають великі прості множники
    if gcd(p - 1, DEFAULT_E) == 1 and gcd(q - 1, DEFAULT_E) == 1:
        logging.debug("Пара простих чисел успішно перевірена")
        return True
    
    logging.warning("Неналежна пара простих чисел для RSA")
    return False

def generate_key_pair(bit_length: int = MIN_BIT_LENGTH) -> Tuple[RSAPublicKey, RSAPrivateKey]:
    """ генерує пару ключів RSA. повертає кортеж (public_key, private_key) """
    if bit_length < MIN_BIT_LENGTH:
        raise ValueError(f"Довжина ключа має бути не менше {MIN_BIT_LENGTH} біт")
    
    logging.info(f"Генерація {bit_length}-бітної пари ключів RSA")
    
    p_q_length = bit_length // 2
    
    while True:
        logging.info(f"Генерація першого простого числа (p) довжиною {p_q_length} біт...")
        p, _ = generate_safe_prime(p_q_length)
        logging.info(f"Згенеровано p: {p}\n")
        
        logging.info(f"Генерація другого простого числа (q) довжиною {p_q_length} біт...")
        q, _ = generate_safe_prime(p_q_length)
        logging.info(f"Згенеровано q: {q}\n")
        
        if not validate_prime_pair(p, q, p_q_length):
            logging.info("Згенеровані прості числа не пройшли валідацію, повторна спроба...")
            continue
        
        n = p * q
        
        if n.bit_length() != bit_length:
            logging.info(f"Згенерований ключ має неправильну довжину ({n.bit_length()} біт), повторна спроба...\n")
            continue
            
        logging.info(f"Обчислено n = p*q: {n}")
        
        phi = (p - 1) * (q - 1)
        logging.info(f"Обчислено φ(n) = (p-1)(q-1): {phi}")
        
        e = DEFAULT_E
        logging.info(f"Використовується e = {e}")
        
        try:
            d = mod_inverse(e, phi)
            logging.info(f"Обчислено d = e^(-1) mod φ(n): {d}")
            
            public_key = RSAPublicKey(e=e, n=n)
            private_key = RSAPrivateKey(d=d, p=p, q=q, n=n)
            
            logging.info("Пара ключів успішно згенерована")
            return public_key, private_key
            
        except ValueError as err:
            logging.warning(f"Помилка обчислення d: {err}, повторна спроба з новими простими числами...")
            continue

# шифрування/розшифрування
def encrypt_block(block: int, public_key: RSAPublicKey) -> int:
    """ шифрує один блок """
    logging.debug(f"Шифрування блоку: {block}")
    if block >= public_key.n:
        raise ValueError("Блок завеликий для даного ключа")
    ciphertext = mod_pow(block, public_key.e, public_key.n)
    logging.debug(f"Зашифрований блок: {ciphertext}")
    return ciphertext

def decrypt_block(block: int, private_key: RSAPrivateKey) -> int:
    """ розшифровує один блок """
    logging.debug(f"Розшифрування блоку: {block}")
    plaintext = mod_pow(block, private_key.d, private_key.n)
    logging.debug(f"Розшифрований блок: {plaintext}")
    return plaintext

def encrypt(message: Union[str, int, RSAMessage], public_key: RSAPublicKey) -> Tuple[List[int], bool, int]:
    """ шифрує повідомлення (текст/число). повертає: (зашифровані_блоки, чи_це_текст, довжина_оригінальних_байтів) """
    if not isinstance(message, RSAMessage):
        message = RSAMessage(message, public_key)
    
    encrypted_blocks = []
    logging.info(f"Шифрування {'текстового' if message.is_text else 'числового'} повідомлення з {len(message.blocks)} блоками")
    
    for i, block in enumerate(message.blocks):
        try:
            encrypted_block = encrypt_block(block, public_key)
            encrypted_blocks.append(encrypted_block)
        except ValueError as e:
            logging.error(f"Помилка шифрування блоку {i + 1}: {str(e)}")
            raise
    
    logging.info("Шифрування завершено")
    return encrypted_blocks, message.is_text, message.original_bytes_length

def decrypt(encrypted_blocks: List[int], private_key: RSAPrivateKey, is_text: bool = False, original_bytes_length: int = 0) -> Union[str, int]:
    """ розшифровує повідомлення """
    block_size = RSAMessage.calculate_block_size(private_key.n)
    decrypted_blocks = []
    
    logging.info(f"Розшифрування {len(encrypted_blocks)} блоку (-ів)")
    print("\nДані для перевірки в RSA калькуляторі:")
    print("----------------------------------------")
    
    for i, block in enumerate(encrypted_blocks):
        print(f"\nБлок {i + 1}:")
        print(f"C (зашифроване повідомлення) = {block}")
        print(f"N (модуль) = {private_key.n}")
        print(f"D (секретний ключ) = {private_key.d}")
        print(f"E (відкритий ключ) = {DEFAULT_E}")
        
        decrypted_block = decrypt_block(block, private_key)
        decrypted_blocks.append(decrypted_block)
        
        print(f"Розшифроване значення = {decrypted_block}")
        print("----------------------------------------")
    
    message = RSAMessage.from_blocks(
        decrypted_blocks, 
        is_text, 
        block_size, 
        original_bytes_length
    )
    return message.original_content

# підпис
def sign(message: Union[str, int, RSAMessage], private_key: RSAPrivateKey) -> List[int]:
    """ створення підпису """
    if not isinstance(message, RSAMessage):
        message = RSAMessage(message, RSAPublicKey(private_key.d, private_key.n))
    
    signatures = []
    logging.info(f"Підписання повідомлення з {len(message.blocks)} блоками")
    
    for i, block in enumerate(message.blocks):
        signature = mod_pow(block, private_key.d, private_key.n)
        signatures.append(signature)
        logging.info(f"Блок {i + 1} підписано: {signature}")
    
    return signatures

def verify(message: Union[str, int, RSAMessage], signatures: List[int], public_key: RSAPublicKey) -> bool:
    """ перевірка підпису """
    if not isinstance(message, RSAMessage):
        message = RSAMessage(message, public_key)
    
    if len(signatures) != len(message.blocks):
        logging.error("Кількість підписів не відповідає кількості блоків повідомлення")
        return False
    
    logging.info(f"Перевірка {len(signatures)} підписів")
    
    for i, (block, signature) in enumerate(zip(message.blocks, signatures)):
        computed = mod_pow(signature, public_key.e, public_key.n)
        if computed != block:
            logging.error(f"Перевірка підпису для блоку {i + 1} не вдалася")
            return False
        logging.info(f"Підпис блоку {i + 1} перевірено")
    
    logging.info("Всі підписи успішно перевірено")
    return True


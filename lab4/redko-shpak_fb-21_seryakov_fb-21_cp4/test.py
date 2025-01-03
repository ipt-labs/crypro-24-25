from rsa import *

def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

def format_key_info(name: str, public_key: RSAPublicKey, private_key: RSAPrivateKey) -> str:
    return f"""
Ключі для {name}:
---------------
Відкритий ключ (e, n):
  e = {public_key.e}
  n = {public_key.n}
  Довжина ключа: {public_key.n.bit_length()} біт
Закритий ключ:
  d = {private_key.d}
  p = {private_key.p}
  q = {private_key.q}
Перевірка:
  e⋅d mod φ(n) = {(public_key.e * private_key.d) % ((private_key.p - 1) * (private_key.q - 1))} (має бути 1)
"""

def demonstrate_key_generation(alice_bit_length, bob_bit_length):
    print_section("ГЕНЕРАЦІЯ КЛЮЧІВ RSA")

    # ключі для аліси
    print(f"1. Генерація ключів для Аліси ({alice_bit_length} біт)...")
    alice_public, alice_private = generate_key_pair(alice_bit_length)
    print(format_key_info("Аліси", alice_public, alice_private))

    # ключі для боба
    print(f"\n2. Генерація ключів для Боба ({bob_bit_length} біт)...")
    bob_public, bob_private = generate_key_pair(bob_bit_length)
    print(format_key_info("Боба", bob_public, bob_private))

    return (alice_public, alice_private), (bob_public, bob_private)

def demonstrate_encryption(alice_keys: Tuple[RSAPublicKey, RSAPrivateKey], bob_keys: Tuple[RSAPublicKey, RSAPrivateKey]):
    print_section("ШИФРУВАННЯ ПОВІДОМЛЕНЬ")

    alice_public, alice_private = alice_keys
    bob_public, bob_private = bob_keys

    test_messages = [
        (12345, "Просте числове повідомлення"),
        (98765432198765432198765432198765432198765432198765432198765432198765432198765432198765432198765432198765432198765432198765432176543219876543219876543217654321987654321987654321,
          "Велике числове повідомлення"),
        ("Привіт, RSA! 🔒", "Простий тест з емодзі"),
        ("Це секретне повідомлення від Боба до Аліси", "Довге повідомлення з кирилицею"),
        ("Test message with special chars: @#$%^&*()", "Тест спеціальних символів")
    ]

    for i, (message, description) in enumerate(test_messages, 1):
        print(f"\nТест {i}.1 - Боб надсилає Алісі:")
        print(f"Опис: {description}")
        print(f"Оригінальне повідомлення: {message}")

        # боб шифрує повідомлення для аліси
        print("\nБоб шифрує повідомлення для Аліси:")
        encrypted_blocks, is_text, orig_len = encrypt(message, alice_public)
        if is_text:
            print(f"Зашифровані блоки: {encrypted_blocks}")
        else:
            print(f"Зашифровані блоки числа: {encrypted_blocks}")

        # аліса розшифровує повідомлення боба
        print("\nАліса розшифровує повідомлення:")
        decrypted = decrypt(encrypted_blocks, alice_private, is_text, orig_len)
        print(f"Розшифроване повідомлення: {decrypted}")
        print(f"Перевірка успішна: {message == decrypted}")

        # аліса відповідає бобу
        reply_message = message * 2 if isinstance(message, int) else f"Re: {message[:20]}... Отримано!"
        print(f"\nТест {i}.2 - Аліса відповідає Бобу:")
        print(f"Оригінальне повідомлення: {reply_message}")

        # аліса шифрує відповідь для боба
        print("\nАліса шифрує повідомлення для Боба:")
        encrypted_reply, reply_is_text, reply_len = encrypt(reply_message, bob_public)
        if reply_is_text:
            print(f"Зашифровані блоки: {encrypted_reply}")
        else:
            print(f"Зашифроване число: {encrypted_reply[0]}")

        # боб розшифровує відповідь аліси
        print("\nБоб розшифровує повідомлення:")
        decrypted_reply = decrypt(encrypted_reply, bob_private, reply_is_text, reply_len)
        print(f"Розшифроване повідомлення: {decrypted_reply}")
        print(f"Перевірка успішна: {reply_message == decrypted_reply}")

        print("\n" + "="*50)

def demonstrate_signature(alice_keys: Tuple[RSAPublicKey, RSAPrivateKey], bob_keys: Tuple[RSAPublicKey, RSAPrivateKey]):
    print_section("ДЕМОНСТРАЦІЯ ЦИФРОВИХ ПІДПИСІВ")

    alice_public, alice_private = alice_keys
    bob_public, bob_private = bob_keys

    test_messages = [
        (12345, "Просте числове повідомлення"),
        (987654321, "Велике числове повідомлення"),
        ("Цей документ засвідчує справжність електронного підпису", "Текстове повідомлення")
    ]

    for i, (message, description) in enumerate(test_messages, 1):
        print(f"\nТест {i}.1 - Підпис від Аліси:")
        print(f"Опис: {description}")
        print(f"Оригінальне повідомлення: {message}")

        # створення підпису алісою
        print("\nАліса створює цифровий підпис:")
        alice_signature = sign(message, alice_private)
        print(f"Підпис: {alice_signature}")

        # перевірка підпису бобом
        print("\nБоб перевіряє підпис Аліси:")
        is_valid = verify(message, alice_signature, alice_public)
        print(f"Підпис валідний: {is_valid}")

        # перевірка на підробку
        print("\nПеревірка виявлення підробки:")
        if isinstance(message, str):
            fake_message = message + " ПІДРОБЛЕНО"
        else:
            fake_message = message + 1
        print(f"Змінене повідомлення: {fake_message}")

        is_valid = verify(fake_message, alice_signature, alice_public)
        print(f"Підпис для зміненого повідомлення валідний: {is_valid}")

        # боб відповідає
        reply_message = message * 2 if isinstance(message, int) else f"Отримав повідомлення: {message}..."
        print(f"\nТест {i}.2 - Боб відповідає підписаним повідомленням:")
        print(f"Повідомлення відповіді: {reply_message}")

        # створення підпису бобом
        print("\nБоб створює цифровий підпис:")
        bob_signature = sign(reply_message, bob_private)
        print(f"Підпис Боба: {bob_signature}")

        # аліса перевіряє підпис боба
        print("\nАліса перевіряє підпис Боба:")
        is_valid = verify(reply_message, bob_signature, bob_public)
        print(f"Підпис валідний: {is_valid}")

        print("\n" + "="*50)

def demonstrate_key_exchange(alice_keys: Tuple[RSAPublicKey, RSAPrivateKey], bob_keys: Tuple[RSAPublicKey, RSAPrivateKey]):
    print_section("ПРОТОКОЛ ОБМІНУ КЛЮЧАМИ")

    alice_public, alice_private = alice_keys
    bob_public, bob_private = bob_keys

    # попередження
    if alice_private.n >= bob_public.n:
        print("\nПопередження: Для оптимальної безпеки модуль Аліси повинен бути менший за модуль Боба")
        print("Продовжуємо демонстрацію...\n")

    # генерація секретного ключа
    secret_key = 12345
    if secret_key >= alice_private.n:
        raise ValueError(f"Ключ k={secret_key} занадто великий для даної криптосистеми")

    print(f"1. Початкові дані:")
    print(f"   Секретний ключ k = {secret_key}")
    print(f"   Відкритий ключ Аліси (e, n) = ({alice_public.e}, {alice_public.n})")
    print(f"   Відкритий ключ Боба (e_1, n_1) = ({bob_public.e}, {bob_public.n})")

    print("\n2. Аліса формує повідомлення:")

    # 1: шифрування ключа
    k1 = mod_pow(secret_key, bob_public.e, bob_public.n)
    print("\n   a) Шифрування ключа k відкритим ключем Боба:")
    print(f"      k_1 = k^(e_1) mod n_1")
    print(f"      k_1 = {secret_key}^{bob_public.e} mod {bob_public.n}")
    print(f"      k_1 = {k1}")

    # 2: створення підпису
    signature = mod_pow(secret_key, alice_private.d, alice_private.n)
    print("\n   б) Створення цифрового підпису своїм закритим ключем:")
    print(f"      S = k^d mod n")
    print(f"      S = {secret_key}^{alice_private.d} mod {alice_private.n}")
    print(f"      S = {signature}")

    # 3: шифрування підпису
    s1 = mod_pow(signature, bob_public.e, bob_public.n)
    print("\n   в) Шифрування підпису відкритим ключем Боба:")
    print(f"      S_1 = S^(e_1) mod n_1")
    print(f"      S_1 = {signature}^{bob_public.e} mod {bob_public.n}")
    print(f"      S_1 = {s1}")

    print("\n3. Передача даних:")
    print(f"   Аліса надсилає Бобу пару чисел (k_1, S_1) = ({k1}, {s1})")

    print("\n4. Боб виконує перевірку отриманих даних:")

    # 4: розшифрування ключа
    received_k = mod_pow(k1, bob_private.d, bob_private.n)
    print("\n   a) Розшифрування k_1 своїм закритим ключем:")
    print(f"      k = k_1^(d_1) mod n_1")
    print(f"      k = {k1}^{bob_private.d} mod {bob_private.n}")
    print(f"      k = {received_k}")

    # 5: розшифрування підпису
    received_signature = mod_pow(s1, bob_private.d, bob_private.n)
    print("\n   б) Розшифрування S_1 своїм закритим ключем:")
    print(f"      S = S_1^(d_1) mod n_1")
    print(f"      S = {s1}^{bob_private.d} mod {bob_private.n}")
    print(f"      S = {received_signature}")

    # 6: перевірка підпису
    verified_k = mod_pow(received_signature, alice_public.e, alice_public.n)
    print("\n   в) Перевірка підпису відкритим ключем Аліси:")
    print(f"      k ?= S^e mod n")
    print(f"      k ?= {received_signature}^{alice_public.e} mod {alice_public.n}")
    print(f"      {verified_k} ?= {received_k}")

    # фінальна перевірка
    signature_valid = (verified_k == received_k == secret_key)
    print("\n5. Результати перевірки:")
    print(f"   Отриманий ключ співпадає з відправленим: {received_k == secret_key}")
    print(f"   Підпис підтверджує справжність ключа: {verified_k == received_k}")
    print(f"   Загальний результат: {'Протокол успішно завершено' if signature_valid else 'Помилка протоколу'}")

def main():
    print("\nДЕМОНСТРАЦІЯ КРИПТОСИСТЕМИ RSA\n")
    print("Цей скрипт демонструє роботу RSA на практичних прикладах")

    # генерація ключів
    alice_keys, bob_keys = demonstrate_key_generation(512, 512)

    # приклад шифрування текст повідомлень
    demonstrate_encryption(alice_keys, bob_keys)

    # приклад підпису
    demonstrate_signature(alice_keys, bob_keys)

    # приклад протоколу обміну ключами
    demonstrate_key_exchange(alice_keys, bob_keys)

    print("\nДЕМОНСТРАЦІЯ ЗАВЕРШЕНА")

if __name__ == "__main__":
    main()

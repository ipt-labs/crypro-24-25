import rsa
from Person import Person

if __name__ == "__main__":

    # Генерація випадкового простого числа для завдання 1
    bit_length = 256
    random_prime_number = rsa.find_prime(bit_length)
    print('\n№1')
    print(f"  Згенеровано випадкове просте число ({bit_length} біт): {random_prime_number}")
    
    key_pair_a, key_pair_b = rsa.generate_key_pairs()
    print('\n№2')
    print("  Пара (p, q) A:", key_pair_a)
    print("  Пара (p1, q1) B:", key_pair_b)
    
    # Генерація RSA-ключів для абонентів A та B
    public_key_a, private_key_a = rsa.rsa_key_generation(key_pair_a[0], key_pair_a[1])
    public_key_b, private_key_b = rsa.rsa_key_generation(key_pair_b[0], key_pair_b[1])
    print('\n№3')
    print("  Відкритий ключ A:", public_key_a)
    print("  Секретний ключ A:", private_key_a)
    print("  Відкритий ключ B:", public_key_b)
    print("  Секретний ключ B:", private_key_b)

    # Приклад шифрування та дешифрування
    print('\n№4')
    message = "Hello, RSA!"
    print(f"Повідомлення для шифрування: {message}")
    encrypted_message = rsa.encrypt(message, public_key_a)
    print(f"Зашифроване повідомлення: {encrypted_message}")
    decrypted_message = rsa.decrypt(encrypted_message, private_key_a)
    print(f"Дешифроване повідомлення: {decrypted_message}")

     # Приклад підпису та перевірки підпису
    signature = rsa.sign_message(message, private_key_a)
    print(f"Підпис повідомлення: {signature}")
    is_valid = rsa.verify_signature(decrypted_message, signature, public_key_a)
    print(f"Перевірка підпису: {'Дійсний' if is_valid else 'Недійсний'}")

     # Приклад перевірки підпису зміненого повідомлення
    is_valid = rsa.verify_signature(decrypted_message + 'a', signature, public_key_a)
    print(f"Перевірка підпису пошкодженого повідомлення: {'Дійсний' if is_valid else 'Недійсний'}")

    print('\n№5')
    # Create two people (sender and receiver)
    alice = Person('Alice')
    bob = Person('Bob')

    #Exchange public keys
    alice.take_friends_key(bob.public_key)
    bob.take_friends_key(alice.public_key)

    # Alice sends a message to Bob
    message = "Hello, Bob!"
    print(f"Аліса пише '{message}' Бобу")
    encrypted_message, encrypted_message_signature = alice.send_message(message)
    print(f"Зашифроване повідомлення: {encrypted_message}")
    print(f"Підпис повідомлення Аліси: {encrypted_message_signature}")

    decrypted_message= bob.receive_message(encrypted_message, encrypted_message_signature)

    if decrypted_message:
        print(f"Боб отримав: {decrypted_message}")
    else:
        print('Повідомлення пошкоджене')

    # Bob sends a message to Alice
    message = "Hello, Alice!"
    print(f"\nБоб пише '{message}' Алісі")
    encrypted_message, encrypted_message_signature = bob.send_message(message)
    print(f"Зашифроване повідомлення: {encrypted_message}")
    print(f"Підпис повідомлення Боб: {encrypted_message_signature}")

    decrypted_message= alice.receive_message(encrypted_message, encrypted_message_signature)

    if decrypted_message:
        print(f"Аліса отримала: {decrypted_message}")
    else:
        print('Повідомлення пошкоджене')
f_name = "txt/text.txt"
keys = ["пр", "иве", "тдру", "гчушь", "какаяодинпроцентс"]

# https://planetcalc.com/2468/
def vig_encrypt(key, text):
    key_len = len(key)
    text_len = len(text)

    if (not (key_len and text_len)):
        return ""
    
    cipher = ""
    for i in range(text_len):
        cipher += chr((ord(text[i]) + ord(key[i % key_len])) % 32 + 1072)
    
    return cipher

# зчитування і фільтрування вхідного тексту
text = ""
with open(f_name, "r", encoding="utf-8") as f:
    for s in f.read().lower():
        if s >= "а" and s <= "я":
            text += s
        elif s == "ё":
            text += "е"
# print(text)

# a = ''.join(chr(s) for s in range(1072, 1104))
# rev_a = ''.join(chr(s) for s in range(1103, 1071, -1))
# print(a)
# print(rev_a)

for k in keys:
    open(f"txt/encrypt_key_{k}.txt", "w").write(vig_encrypt(k, text))

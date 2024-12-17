import json

obj_for_json = list()

alph = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def findBigrams(text):
    bigrams = dict()

    for i in alph:
        for j in alph:
            bigrams[i + j] = 0

    for i in range(0, len(text) - 1, 2):
        item = text[i] + text[i + 1]
        if item in bigrams.keys():
            bigrams[item] += 1

    bigrams_count = sum(bigrams.values())

    for key, val in bigrams.items():
        bigrams[key] = val / bigrams_count

    return bigrams

def solveEquation(a, b, m):
    gcd, _, _ = invertElement(a, m)

    if gcd == 1:
        _, _, elem = invertElement(a, m)
        # res = b * (elem % m) % m
        return b * elem % m
    elif gcd > 1 and b % gcd == 0:
        _, _, elem = invertElement(int(a / gcd), int(m / gcd))
        first = int(b / gcd * elem % m)
        return [first + int(m / gcd) * i for i in range(gcd)]

# a < b
def invertElement(a, b):
    if a == 0:
        return b, 1, 0

    gcd, prev_u, curr_u = invertElement(b % a, a)
    new_u = prev_u - (b // a) * curr_u

    return gcd, curr_u, new_u

def decrypt(text, a, b):
    _, _, elem_a = invertElement(a, 31**2)
    line = ""
    if elem_a is not None:
        for i in range(0, len(text) - 1, 2):
            val_y = alph.index(text[i]) * 31 + alph.index(text[i + 1])
            res_x = (elem_a * (val_y - b)) % 31**2
            line += alph[res_x // 31] + alph[res_x % 31]
    print(f"a: {a}, b: {b} -> {line[:30]}...")

    obj = {"a": a, "b": b, "text": line}
    obj_for_json.append(obj)

def filter_text(text):
    filter_symb = ["\n", " "]

    for item in filter_symb:
        text = text.replace(item, "")
    
    return text

def main():
    bigrams = ["ст", "но", "то", "на", "ен"]

    with open("text.txt", "r", encoding = "utf-8") as file:
        text = filter_text(file.read())
        text_bigrams = list(dict(sorted(findBigrams(text).items(), key=lambda x: x[1], reverse = True)).keys())[:5]
        
        print(text_bigrams)

        o_val, c_val = [], []
        for i in range(len(text_bigrams)):
            o_val.append(alph.index(bigrams[i][0]) * 31 + alph.index(bigrams[i][1]))
            c_val.append(alph.index(text_bigrams[i][0]) * 31 + alph.index(text_bigrams[i][1]))

        all_bigrams = []
        for i in o_val:
            for j in c_val:
                all_bigrams.append((i, j))

        print(all_bigrams)

        print("-" * 30)

        key_dict = dict()
        for i in range(len(all_bigrams)):
            for j in range(len(all_bigrams)):
                if all_bigrams[i][0] != all_bigrams[j][0] and all_bigrams[i][1] != all_bigrams[j][1]:
                    a = solveEquation(all_bigrams[i][0] - all_bigrams[j][0] % 31**2, all_bigrams[i][1] - all_bigrams[j][1] % 31**2, 31**2)
                    if a != None and not isinstance(a, list):
                        key_dict[a] = (all_bigrams[i][1] - a * all_bigrams[i][0]) % 31**2
                    elif a != None and isinstance(a, list):
                        for item in a:
                            key_dict[item] = (all_bigrams[i][1] - item * all_bigrams[i][0]) % 31**2
        
        for a, b in key_dict.items():
            decrypt(text, a, b)
        
if __name__ == "__main__":
    main()

    with open("text.json", "w") as f:
        json.dump(obj_for_json, f, ensure_ascii=False, indent=4)
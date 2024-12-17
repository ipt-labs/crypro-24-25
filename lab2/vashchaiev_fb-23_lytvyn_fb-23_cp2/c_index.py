import os
import sys
import matplotlib.pyplot as plt

def count_symbols(text):
    letters = dict()

    for item in text:
        if item not in letters.keys():
            letters[item] = 1
        else:
            letters[item] += 1

    return letters

def c_indx(text):
    l = len(text)
    if l < 2:return 0
    s = 0
    
    for f in count_symbols(text).values():
        s += f * (f -1)

    return s / (l * (l -1))

try:
    f_list = os.listdir(sys.argv[1])
except (FileNotFoundError, NotADirectoryError, IndexError):
    print("No such directory.")
    exit()

dt = {}
offset = len(max(f_list, key=len))+10
print(f"{'Files' :<{offset}} Values")
print("-" * (offset +20))
for file in f_list:
    if ".txt" in file:
        p_file = f"{sys.argv[1]}/{file}"
        t = open(p_file, "r").read()
        print(f"{p_file :<{offset}} {c_indx(t)}")
        if "encrypt_key" in file:
            dt[f'{len(file[12:-4])}'] = c_indx(t)

plt.bar(dt.keys(), dt.values())
plt.xlabel('Довжина ключа')
plt.ylabel('Значення I(Y)')
plt.title('Залежність I(Y) від довжини ключа')
plt.ylim(min(dt.values()) *0.95, max(dt.values()) *1.03)
plt.show()


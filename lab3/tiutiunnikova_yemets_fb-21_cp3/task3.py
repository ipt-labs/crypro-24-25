#-------АЛГОРИТМ ЕВКЛІДА------------------------
def gcd_evc(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = gcd_evc(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

#-------ОБЕРНЕНИЙ ЗА МОДУЛЕМ------------------------
def obratn(a, m):
    gcd, x, _ = gcd_evc(a, m)
    if gcd != 1:
        return None  
    return x % m 

#-------ЛІНІЙНІ ПОРІВНЯННЯ------------------------
def congr(a, b, m):
    gcd, x, y = gcd_evc(a, m)    
    if b % gcd != 0:
        return []   
    a_ = a // gcd
    b_ = b // gcd
    m_ = m // gcd
    
    obratn_a = obratn(a_, m_)   
    if obratn_a is None:
        return []
    
    x0 = (obratn_a * b_) % m_
    answers = []
    for i in range(gcd):
        answers.append(x0 + i * m_)   
    return answers


#----------------БІГРАМИ---------------------------
ct_bis = ['вн', 'тн', 'дк', 'ун', 'хщ']
tv_bis = ['ст', 'но', 'то', 'на', 'ен']
alph = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
ct_num = {ch: i for i, ch in enumerate(alph)}
num_ct = {i: ch for i, ch in enumerate(alph)}
m2 = 961

pairs = [(tv_bi, ct_bi)
            for tv_bi in tv_bis
            for ct_bi in ct_bis]

n_pairs = [(31 * ct_num[pair[0][0]] + ct_num[pair[0][1]], 
            31 * ct_num[pair[1][0]] + ct_num[pair[1][1]]) for pair in pairs]

#------------------КЛЮЧІ----------------------------------
keys = []
for i in range(len(n_pairs)):
    x1, y1 = n_pairs[i]

    for j in range(i + 1, len(n_pairs)):
        x2, y2 = n_pairs[j]
        razn_x = x1 - x2
        razn_y = y1 - y2
        if razn_x == 0:
            continue

        answer = congr(razn_x, razn_y, m2)
        if answer:
            for x in answer:
                a = x
                b = (y1 - a * x1) % m2
                keys.append((a, b))

print("\nКандидати (a, b):")
for key in keys:
    print(key)

#------------------РОЗШИФРУВАННЯ------------------------------------
with open('05.txt', 'r') as f:
    text = f.read().replace('\n', '')
nums = [ct_num[ch] for ch in text] 

def decrypt(nums, a, b, m):
    m2 = m ** 2
    vt = []  

    a_obr = obratn(a, m2)
    
    if a_obr is None: 
        return None

    for i in range(0, len(nums), 2): 
        y = nums[i] 

        if i < len(nums) - 1:
            n_y = nums[i + 1]
        else:
            n_y = 0

        idx = y * 31 + n_y 
        x = (a_obr * (idx - b)) % m2 
        x1, x2 = (x // 31), (x % 31)  

        vt.append(num_ct[x1 % m])  
        vt.append(num_ct[x2 % m])  

    return ''.join(vt)


full_vt = {}
for a, b in keys:
    decr = decrypt(nums, a, b, len(alph))
    if decr:
        full_vt[(a, b)] = decr
        
nopop_bis = ["мэ", "хэ", "бц", "оэ", "фм", "вщ", "иэ", "бб", "эм", "бт", "фк", "ыя", "ыц", "дщ", "нж", "лщ", "эг", "уу", "фс"]

def bis(text):
    return [text[i:i+2] for i in range(0, len(text), 2)]

def count(text, nopop_bis):
    bi = bis(text)
    return sum(1 for b in bi if b in nopop_bis)

bis_fr = {}
for key, vt in full_vt.items():
    fr_nopop = count(vt, nopop_bis)
    bis_fr[key] = fr_nopop
bisort = sorted(bis_fr.items(), key=lambda x: x[1])

print("Ключі з найменшою кількість непоширених біграм:")
for i, (key, fr_nopop) in enumerate(bisort[:10]):
    print(f"{i+1}. Ключ {key} - Кількість непоширених біграм: {fr_nopop}")
    
result = (654, 777)
print(full_vt[result])

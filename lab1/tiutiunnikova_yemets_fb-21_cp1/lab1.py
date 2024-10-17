import re
import pandas as pd
import numpy as np

# ---------ФІЛЬТРАЦІЯ--------------
def filt(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', re.sub(r'[^а-яё\s]', ' ', text)).strip()
    return text

#----------УНІГРАМИ-----------------
def uni_calc(text, no_space=False):
    text = filt(text)
    if no_space:
        text = text.replace(' ', '')

    fr_count = {}
    vsego_uni = 0
    for char in text:
        if 'а' <= char <= 'я' or char == 'ё':
            if char in fr_count:
                fr_count[char] += 1
            else:
                fr_count[char] = 1
            vsego_uni += 1
        elif char == ' ':
            if ' ' in fr_count:
                fr_count[' '] += 1
            else:
                fr_count[' '] = 1
            vsego_uni += 1

    uni_fr = {char: cnt / vsego_uni for char, cnt in fr_count.items()}
    return uni_fr

#-----------БІГРАМИ--------------------
def bi_calc(text, no_space=False):
    text = filt(text)  
    if no_space:
        text = text.replace(' ', '')
    
    bi_count = {}
    total_bis = 0

    #--------ПЕРЕТИНАЮЧІ-------------------
    for i in range(0, len(text) - 1):
        bi = text[i:i+2]
        if len(bi) == 2:
            if bi in bi_count:
                bi_count[bi] += 1
            else:
                bi_count[bi] = 1
            total_bis += 1

    bi_fr = {bi: cnt / total_bis for bi, cnt in bi_count.items()}

    #--------НЕПЕРЕТИНАЮЧІ-------------------
    bi_no_count = {}
    total_bis_no = 0
    for i in range(0, len(text) - 1, 2):
        bi = text[i:i+2]
        if len(bi) == 2:
            if bi in bi_no_count:
                bi_no_count[bi] += 1
            else:
                bi_no_count[bi] = 1
            total_bis_no += 1

    bi_no_fr = {bi: cnt / total_bis_no for bi, cnt in bi_no_count.items()}
    return bi_fr, bi_no_fr

#---------------ЕНТРОПІЯ------------------
def calc_ent(fr):
    ent = -sum(p * np.log2(p) for p in fr.values() if p > 0)
    return ent

def calc_ent_H2(fr):
    ent = (-sum(p * np.log2(p) for p in fr.values() if p > 0))*0.5
    return ent


#---------------НАДЛИШКОВІСТЬ--------------
def calc_r(ent, max_ent):
    return 1 - (ent / max_ent)

#---------------ЗБЕРЕЖЕННЯ-----------------
def save(fr_uni_s, fr_uni_nos, fr_bi_s_per, fr_bi_nos_per, fr_bi_s_noper, fr_bi_nos_noper, file_name):
    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:

        df_uni_s = pd.DataFrame(list(fr_uni_s.items()), columns=['Літера', 'Частота'])
        df_uni_s = df_uni_s.sort_values(by='Частота', ascending=False)
        df_uni_s.to_excel(writer, sheet_name='Уніграми з пробілами', index=False)
        
        df_uni_nos = pd.DataFrame(list(fr_uni_nos.items()), columns=['Літера', 'Частота'])
        df_uni_nos = df_uni_nos.sort_values(by='Частота', ascending=False)
        df_uni_nos.to_excel(writer, sheet_name='Уніграми без пробілів', index=False)
        
        df_bg_s = pd.DataFrame(list(fr_bi_s_per.items()), columns=['Біграма', 'Частота'])
        df_bg_s = df_bg_s.sort_values(by='Частота', ascending=False)
        df_bg_s.to_excel(writer, sheet_name='Перетинаючі біграми з пробілами', index=False)

        df_bi_nos_per = pd.DataFrame(list(fr_bi_nos_per.items()), columns=['Біграма', 'Частота'])
        df_bi_nos_per = df_bi_nos_per.sort_values(by='Частота', ascending=False)
        df_bi_nos_per.to_excel(writer, sheet_name='Перетинючі біграми без пробілів', index=False)
        
        df_bi_nos_noper = pd.DataFrame(list(fr_bi_s_noper.items()), columns=['Біграма', 'Частота'])
        df_bi_nos_noper = df_bi_nos_noper.sort_values(by='Частота', ascending=False)
        df_bi_nos_noper.to_excel(writer, sheet_name='Неперетинаючі біграми з пробілами', index=False)

        df_bi_nos_noper = pd.DataFrame(list(fr_bi_nos_noper.items()), columns=['Біграма', 'Частота'])
        df_bi_nos_noper = df_bi_nos_noper.sort_values(by='Частота', ascending=False)
        df_bi_nos_noper.to_excel(writer, sheet_name='Неперетинаючі біграми без пробілів', index=False)

#---------------------------ОСНОВНА ЧАСТИНА-------------------------
path = 'text.txt'
with open(path, 'r') as file:
    text = file.read()

fr_uni_s = uni_calc(text)
fr_bi_s_per, fr_bi_s_noper = bi_calc(text)

fr_uni_nos = uni_calc(text, no_space=True)
fr_bi_nos_per, fr_bi_nos_noper = bi_calc(text, no_space=True)

ent_uni_s = calc_ent(fr_uni_s)
ent_uni_nos = calc_ent(fr_uni_nos)
ent_bi_s_per = calc_ent_H2(fr_bi_s_per)
ent_bi_nos_per = calc_ent_H2(fr_bi_nos_per)
ent_bi_s_noper = calc_ent_H2(fr_bi_s_noper)
ent_bi_nos_noper = calc_ent_H2(fr_bi_nos_noper)

max_ent_sp = np.log2(33)
max_ent_nosp = np.log2(32)

r_uni_s = calc_r(ent_uni_s, max_ent_sp)
r_uni_nos = calc_r(ent_uni_nos, max_ent_nosp)
r_bi_s_per = calc_r(ent_bi_s_per, max_ent_sp)
r_bi_nos_per = calc_r(ent_bi_nos_per, max_ent_nosp)
r_bi_s_noper = calc_r(ent_bi_s_noper, max_ent_sp)
r_bi_nos_noper = calc_r(ent_bi_nos_noper, max_ent_nosp)

print(f'H1 (уніграм з пробілами): {ent_uni_s:.6f}')
print(f'Н1 (уніграм без пробілів): {ent_uni_nos:.6f}')
print(f'Н2 (біграм з пробілами): {ent_bi_s_per:.6f}')
print(f'Н2 (біграм без пробілів): {ent_bi_nos_per:.6f}')
print(f'Н2 (неперетинаючих біграм з пробілами): {ent_bi_s_noper:.6f}')
print(f'Н2 (неперетинаючих біграм без пробілів): {ent_bi_nos_noper:.6f}')

print(f'R (уніграм з пробілами): {r_uni_s:.6f}')
print(f'R (уніграм без пробілів): {r_uni_nos:.6f}')
print(f'R (біграм з пробілами): {r_bi_s_per:.6f}')
print(f'R (біграм без пробілів): {r_bi_nos_per:.6f}')
print(f'R (неперетинаючих біграм з пробілами): {r_bi_s_noper:.6f}')
print(f'R (неперетинаючих біграм без пробілів): {r_bi_nos_noper:.6f}')

save(fr_uni_s, fr_uni_nos, fr_bi_s_per, fr_bi_nos_per, fr_bi_s_noper, fr_bi_nos_noper, './lab1.xlsx')

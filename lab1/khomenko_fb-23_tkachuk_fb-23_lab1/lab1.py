import pandas as pd
import math

alphabet_space = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
raw_text=open('lab1.txt', encoding='utf-8').read().replace('n','').replace('\n',' ').lower()
text=''.join(char for char in raw_text if char in alphabet and char.isalpha())
text_space=''.join(char for char in raw_text if char in alphabet_space and char.isalpha() or char.isspace())

# Кількість та частота (ймовірність) букв

def find_letter_frequency_and_count(text:str,alphabet:str):

    letter_count_dict={}
    for c in text:
        letter_count_dict[c]=letter_count_dict.get(c,0)+1

    letter_frequency_dict={}
    for c in letter_count_dict:
        letter_frequency_dict[c]=round(letter_count_dict[c]/len(text),5)
    return letter_count_dict, letter_frequency_dict

# Без пробілу
letter_count,letter_frequency=find_letter_frequency_and_count(text,alphabet)
df_letter_frequency = pd.DataFrame({
    'Letter': letter_frequency.keys(),
    'Count': [letter_count[c] for c in letter_frequency.keys()],
    'Frequency': letter_frequency.values()
})
df_letter_frequency = df_letter_frequency.sort_values(by='Frequency', ascending=False)
print(df_letter_frequency)
df_letter_frequency.to_excel("Amount_without_space.xlsx")

# З пробілом
letter_count_space,letter_frequency_space=find_letter_frequency_and_count(text_space,alphabet_space)
df_letter_frequency = pd.DataFrame({
    'Letter': letter_frequency_space.keys(),
    'Count': [letter_count_space[c] for c in letter_frequency_space.keys()],
    'Frequency': letter_frequency_space.values()
})
df_letter_frequency = df_letter_frequency.sort_values(by='Frequency', ascending=False)
print(df_letter_frequency)
df_letter_frequency.to_excel("Amount_with_space.xlsx")

# Кількість і частота (ймовірність) біграм 
def find_bigram_frequency_and_count(text:str, alphabet:str, cross:bool):
    bigram_count_dict={}
    bigram_frequency_dict={}
    if cross:
        for i in range(len(text)-1):
            key=text[i]+text[i+1]
            bigram_count_dict[key] = bigram_count_dict.get(key,0) + 1
        for key in bigram_count_dict.keys():
            bigram_frequency_dict[key]=round(bigram_count_dict[key]/(len(text)-1),5)
    if not cross:
        for i in range(0,len(text)-1,2):
            key=text[i]+text[i+1]
            bigram_count_dict[key] =bigram_count_dict.get(key,0) + 1
        for key in bigram_count_dict.keys():
            bigram_frequency_dict[key]=round(bigram_count_dict[key]/(len(text)/2),5) 
    return  bigram_count_dict, bigram_frequency_dict

def bigram_table(alphabet:str,b_f:dict,write_to_xlsx:bool,filename='df'):
    alpfil=sorted(alphabet)
    df=pd.DataFrame(index=alpfil,columns=alpfil)
    bigramlist=b_f.keys()
    for i in b_f.keys():
        x=alpfil.index(i[0])
        y=alpfil.index(i[1])
        df.iloc[x,y]=b_f[i]
    if " " in df.index:
        df=df.rename(index={" ": "пробіл"},columns={" ": "пробіл"})
    if write_to_xlsx:
        df.to_excel(f"{filename}.xlsx")
    return df

# Без пробілу для пересічної біграми
bigram_count_cross,bigram_frequency_cross=find_bigram_frequency_and_count(text,alphabet,True)
bigram_cross_table=bigram_table(alphabet,bigram_frequency_cross,True,'bigram_cross_table')
print(bigram_cross_table)

# З пробілом для пересічної біграми
bigram_count_cross_space,bigram_frequency_cross_space=find_bigram_frequency_and_count(text_space,alphabet_space,True)
bigram_cross_space_table=bigram_table(alphabet_space,bigram_frequency_cross_space,True,'bigram_cross_space_table')
print(bigram_cross_space_table)

# Без пробілу для непересічної біграми
bigram_count_nocross,bigram_frequency_nocross=find_bigram_frequency_and_count(text,alphabet,False)
bigram_nocross_table=bigram_table(alphabet,bigram_frequency_nocross,True,'bigram_nocross_table')
print(bigram_nocross_table)

# З пробілом для непересічної біграми
bigram_count_nocross_space,bigram_frequency_nocross_space=find_bigram_frequency_and_count(text_space,alphabet_space,False)
bigram_nocross_space_table=bigram_table(alphabet_space,bigram_frequency_nocross_space,True,'bigram_nocross_space_table')
print(bigram_cross_space_table)

# H1
def h1_entropy(letter_frequency):
    preh1=[]
    for f in letter_frequency.values():
        preh1.append(-f*math.log(f,2))
    preh1= sorted(preh1,reverse=1)
    H1=sum(preh1)
    return H1

h1_space=h1_entropy(letter_frequency_space)
h1=h1_entropy(letter_frequency)
print(f"Питома ентропія на символ монограми: {h1}")
print(f"Питома ентропія на символ монограми(з пробілом): {h1_space}")
# H2
def h2_entropy(bigram_frequency):
    preh2 = []
    for f in bigram_frequency.values():
        if f != 0:
            preh2.append(-f * math.log(f, 2))
    preh2 = sorted(preh2, reverse=1)
    H2 = sum(preh2)/2
    return H2

h2_crossed=h2_entropy(bigram_frequency_cross)
h2_crossed_space=h2_entropy(bigram_frequency_cross_space)

h2_nocrossed=h2_entropy(bigram_frequency_nocross)
h2_nocrossed_space=h2_entropy(bigram_frequency_nocross_space)

print(f"Питома ентропія на символ пересічної біграми: {h2_crossed}")
print(f"Питома ентропія на символ пересічної біграми(з пробілом): {h2_crossed_space}")
print(f"Питома ентропія на символ непересічної біграми: {h2_nocrossed}")
print(f"Питома ентропія на символ непересічної біграми(з пробілом): {h2_nocrossed_space}")

# Надлишковість російської мови
def r(h,alphabet):
    h0=math.log2(len(alphabet))
    r=1-(h/h0)
    return r

r1=r(h1,alphabet)
r1_space=r(h1_space,alphabet_space)

r2_cross=r(h2_crossed,alphabet)
r2_cross_space=r(h2_crossed_space,alphabet_space)

r2_nocross=r(h2_nocrossed,alphabet)
r2_nocross_space=r(h2_nocrossed_space,alphabet_space)

print(f"Надлишковість для монограми: {r1}")
print(f"Надлишковість для монограми(з пробілом): {r1_space}")

print(f"Надлишковість для пересічної біграми: {r2_cross}")
print(f"Надлишковість для пересічної біграми(з пробілом): {r2_cross_space}")
print(f"Надлишковість для непересічної біграми: {r2_nocross}")
print(f"Надлишковість для непересічної біграми(з пробілом): {r2_nocross_space}")
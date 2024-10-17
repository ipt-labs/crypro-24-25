#This script helps us with finding the key after we know its length
#Preferably used with IDLE

alphabetlength=32
plaincommon=["о", "е", "а", "и", "н", "т", "с", "л", "в", "р", "к", "м", "п", "ы", "у", "б", "я", "ь", "г", "з", "ч", "й", "ж", "х", "ш", "ю", "ц", "э", "щ", "ф", "ъ"]

def RusLowerCharToInt(ch):
    return ord(ch)-0x430

def IntToRusLowerChar(i):
    return chr(i+0x430)

def GetKey(frequencies, c=0):
    key=u""
    for i in range(0, r):
        y=frequencies[i].index(max(frequencies[i]))
        keychar=(y - RusLowerCharToInt(plaincommon[c])) % alphabetlength
        key+=IntToRusLowerChar(keychar)
    return key

def Decrypt(data, key):
    plaintext=u""
    keylen=len(key)
    for i in range(len(data)):
        plainchar=(RusLowerCharToInt(data[i]) - RusLowerCharToInt(key[i%keylen])) % alphabetlength
        plaintext+=IntToRusLowerChar(plainchar)
    return plaintext


file=open('./input.txt', 'r', encoding="utf-8")
data=file.read().replace('\n', '').lower()

r=17

frequencies=[[0]*alphabetlength for i in range(r)]

for i in range(0, r):
    j=i
    l=len(data)
    while(j<l):
        frequencies[i][RusLowerCharToInt(data[j])]+=1
        j+=r

key=GetKey(frequencies, 0)

print("Calculated key (from the most common letter): %s" % key)
plaintext=Decrypt(data, key)
print(plaintext)

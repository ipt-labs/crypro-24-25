from congruencesolver import CongruenceSolve
import lab1
from collections import OrderedDict
import os.path

alphabet = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ы", "э", "ю", "я"]
vowels = ["а", "е", "и", "й", "о", "у", "ы", "ь", "э", "ю", "я"]
commonbigrams = ["ст", "но", "то", "на", "ен"]

m=31

def BigramToInt(a):
    return alphabet.index(a[0])*m + alphabet.index(a[1])

def IntToBigram(i):
    return alphabet[(i-i%m)%(m**2)//m] + alphabet[i%m]

def Decrypt(file, a, b):
    result=""
    if (os.path.isfile(file)):
        with open(file, "r", encoding="utf-8") as InputFile:
            InputFile.seek(0)
            if (i == 1):
                InputFile.read(1)
            while True:
                char = InputFile.read(2).lower()
                #print(char)
                if ((len(char) == 2) and (char[0] in alphabet) and (char[1] in alphabet)):
                    l=CongruenceSolve(a,(BigramToInt(char)-b)%m**2,m**2)
                    if(len(l)!=1):
                        return ""
                    result=result+IntToBigram(l[0])

                if not char:
                    break
    return result

def ImpossibleBigrams():
    impossible=list()
    for i in vowels:
        impossible.append(i+"ь")
        impossible.append(i+"ы")
    return impossible

def CountImpossibleBigrams(text):
    impossible=ImpossibleBigrams()
    count=0
    i=0
    while(i<len(text)-1):
        char=text[i:i+2]
        if char in impossible:
            count+=1
        i+=2
    return count
    

if __name__ == "__main__":
    lab1.PreprocessText(alphabet, "./09.txt", "./out.txt", False)
    P2 = lab1.CalculateBigramFrequency("./out.txt", alphabet, False)
    P2 = OrderedDict(sorted(P2.items(), key=lambda kv: kv[1][0], reverse=True))
    cipherbigrams=list(P2.keys())[0:len(commonbigrams)]
    print(cipherbigrams)
    keys = list()
    for i in range(len(commonbigrams)):
        commonbigrams[i]=BigramToInt(commonbigrams[i])
        cipherbigrams[i]=BigramToInt(cipherbigrams[i])
    for i in range(len(commonbigrams)):
        for j in range(len(commonbigrams)):
            for x in range(len(cipherbigrams)):
                for y in range(len(cipherbigrams)):
                    if i == j or x == y:
                        continue
                    a = CongruenceSolve((commonbigrams[i]-commonbigrams[j])%m**2, (cipherbigrams[x]-cipherbigrams[y])%m**2, m**2)
                    if len(a)==1:
                        a=a[0]
                        b=(cipherbigrams[x]-a*commonbigrams[i])%m**2
                        if (a,b) not in keys:
                            text = Decrypt("./out.txt", a, b)
                            if text != "" and CountImpossibleBigrams(text)==0:
                                keys.append((a, b))
    print("Possible keys: "+str(keys))
                        
    

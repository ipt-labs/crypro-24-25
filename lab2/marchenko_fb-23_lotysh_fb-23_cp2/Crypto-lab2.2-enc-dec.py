# Marchenko Rodion Cryptography lab №2.1 Vigenere scipher encoder-decoder program:

import math
import os.path
import sys
import pandas as pd

BOLD = "\033[1m"
END = "\033[0m"
RED = "\033[0;31m"

Latin = "abcdefghijklmnopqrstuvwxyz"
Cyrilic1 = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
Cyrilic2 = "абвгдежзиіїйклмнопрстуфхцчшщьєюя"

def PrintHelp():
    print("Vigenere scipher encoder / decoder. Usage:\n\t -e <OpenText> - Encrypt a .TXT message file \n\t -d <EncryptedText> - Decrypt a .TXT scipher file\n\t -k <Key> - Provide an encryption key \n\t -a <Alphabet> - EN or UA or RU (default == RU)\n\t -s - include spaces \n\t -h - help \n")



#This function turns a raw .TXT text file into a sequence of space-separated lowercase words
# and returns the number of characters in the created file
def PreprocessText(AllowedChars, InputFileName, AllowNewLines = True):
    
    FormerChar = " "
    OutputBuff = ""
    cnt = 0
    if (os.path.isfile(InputFileName)):
        with open(InputFileName, "r", encoding="utf-8") as InputFile:
            Notfirst = True
            while True:
                char = InputFile.read(1).lower()
                if (AllowNewLines == False and char == "\n"): #Process newlines
                    char = " "
                elif (char == "ё"): #Normalize characters
                    char = "е"
                if (char in AllowedChars):
                    if ((char != " ") or (char == " " and FormerChar != " ")): #Multiple spaces in a row prevention
                        OutputBuff = OutputBuff + char
                        FormerChar = char
                        cnt = cnt + 1    
                if not char: 
                    break
                    
            InputFile.close()

    return [OutputBuff, cnt]


#This function generates a dict of reference ordinals for every alphabet letter
def GenOrdinals(Alphabet):
    LetterArray = list(Alphabet)
    OrdinalDict = {}
    for i in range(0, len(LetterArray)):
        OrdinalDict.update({LetterArray[i]: i})
    return OrdinalDict


#This function expands a given word key to the encrypted message length
def ExpandKey(Textlen, OriginalKey):
    if(len(OriginalKey) >= Textlen):
        return OriginalKey
    else:
        return OriginalKey * (math.floor(Textlen / len(OriginalKey)) + 1)
        

#Vigenere scipher encryption function
def VigenereEncrypt(OutputFileName, TextBuff, ExpandedKey, Alphabet):
    OrdinalDict = GenOrdinals(Alphabet)

    with open(OutputFileName, "w", encoding="utf-8") as OutputFile:
        for i in range(0, len(TextBuff)):
            EncryptedCharOrdinal = (OrdinalDict[TextBuff[i]] + OrdinalDict[ExpandedKey[i]]) % len(OrdinalDict)
            OutputFile.write(Alphabet[EncryptedCharOrdinal])

        OutputFile.close()
    

#Vigenere scipher decryption function
def VigenereDecrypt(OutputFileName, TextBuff, ExpandedKey, Alphabet):
    OrdinalDict = GenOrdinals(Alphabet)

    with open(OutputFileName, "w", encoding="utf-8") as OutputFile:
        for i in range(0, len(TextBuff)):
            DecryptedCharOrdinal = (OrdinalDict[TextBuff[i]] - OrdinalDict[ExpandedKey[i]]) % len(OrdinalDict)
            OutputFile.write(Alphabet[DecryptedCharOrdinal])

        OutputFile.close()



##### Driver code: #####
argc = len(sys.argv)
In = ""
Key = ""
Alfa = Cyrilic1
Encrypt = True

#Parse agruments from console based on preceding parameters:
if (argc == 1 or argc % 2 == 0 or argc > 9 or (argc == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help"))):
    PrintHelp()
elif(argc > 2):

    print(RED+"""
╔════════════════════════════════════════════════════╗
║ EN/UA/RU Vigenere scipher .TXT encryptor-decryptor ║
╚════════════════════════════════════════════════════╝
    """+END)

    for i in range(0, argc):
        if(sys.argv[i] == "-e" and i + 1 < argc):
            In = sys.argv[i + 1]
        elif(sys.argv[i] == "-d" and i + 1 < argc):
            In = sys.argv[i + 1]
            Encrypt = False
        elif(sys.argv[i] == "-k" and i + 1 < argc):
            Key = sys.argv[i + 1].lower()
        elif(sys.argv[i] == "-a" and i + 1 < argc):
            if (sys.argv[i + 1] == "EN" or sys.argv[i + 1] == "en"):
                Alfa = Latin
            if (sys.argv[i + 1] == "UA" or sys.argv[i + 1] == "ua"):
                Alfa = Cyrilic2
        elif(sys.argv[i] == "-s" and i + 1 < argc):
            Alfa = Alfa + " "

    if (In == "" or Key == ""):
        PrintHelp()
    else:
        #Create output file names:
        if(In.lower()[-4:] == ".txt"):
            Out = In[:-4] + "-VIGENERE.txt"
            Plain = In[:-4] + "-PLAINTEXT.txt"
            Dec = In[:-4] + "-DEC.txt"
        else:
            Out = In + "-VIGENERE.txt"
            Plain = In + "-PLAINTEXT.txt"
            Dec = In + "-DEC.txt"

        #Encrypt or decrypt data here:
        TextValues = PreprocessText(Alfa, In, False)
        OutputBuff = TextValues[0]
        Textlen  = TextValues[1]
        if (Textlen > 0):
            ExpandedKey = ExpandKey(Textlen, Key)
            if(Encrypt == True):
                VigenereEncrypt(Out, OutputBuff, ExpandedKey, Alfa)
                print("Encrypted text message of "+BOLD+str(Textlen)+END+" Characters using key \""+Key+"\".")
                with open(Plain, "w", encoding="utf-8") as PlaintextFile:
                    PlaintextFile.write(OutputBuff) #Output stripped plaintext too.
                    PlaintextFile.close()

            else:
                VigenereDecrypt(Dec, OutputBuff, ExpandedKey, Alfa)
                print("Decrypted text message of "+BOLD+str(Textlen)+END+" Characters using key \""+Key+"\".")

        else:
            print("ERROR: Empty input file provided!\n")
            







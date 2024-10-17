# Marchenko Rodion Cryptography lab №1

import math
import os.path
import sys
import pandas as pd

BOLD = "\033[1m"
END = "\033[0m"
YELLOW = "\033[1;33m"



#This function turns a raw .TXT text file into a sequence of space-separated lowercase words
def PreprocessText(AllowedChars, InputFileName, OutputFileName, AllowNewLines = True):
    
    FormerChar = " "
    if (os.path.isfile(InputFileName)):
        with open(InputFileName, "r", encoding="utf-8") as InputFile:
            with open(OutputFileName, "w", encoding="utf-8") as OutputFile:
                Notfirst = True
                while True:
                    char = InputFile.read(1).lower()
                    if (AllowNewLines == False and char == "\n"): #Process newlines
                        char = " "
                    elif (char == "ё"): #Normalize characters
                        char = "е"
                    elif (char == "ъ"):
                        char = "ь"
                    if (char in AllowedChars):
                        if ((char != " ") or (char == " " and FormerChar != " ")): #Multiple spaces in a row prevention
                            OutputFile.write(char)
                            FormerChar = char    
                    if not char: 
                        break
                    
                OutputFile.close()
                InputFile.close()


#This function calculates the number of occurences and frequency in text of single letters from CharArray 
def CalculateSingleLetterFrequency(InputFileName, CharArray):    
    
    ResultDict = {}
    Sum = 0
    for i in range(0, len(CharArray)):
        ResultDict.update({CharArray[i]: [0,0]})

    if (os.path.isfile(InputFileName)):
        with open(InputFileName, "r", encoding="utf-8") as InputFile:
            while True:
                char = InputFile.read(1).lower()
                if (char in CharArray):
                    ResultDict.update({char: [ResultDict[char][0] + 1,0]})
                    Sum = Sum + 1
                
                if(Sum % 10 == 0):
                    print("Processing char № "+YELLOW+BOLD+str(Sum)+END+END, end='\r')
                    
                if not char:
                    print("\n")
                    print(YELLOW+BOLD+"Processing of single characters completed!"+END+END, end='\r')
                    break
                
            InputFile.close()
            for key in ResultDict.keys():
                Probability = round(ResultDict[key][0] / Sum, 8)
                ResultDict.update({str(key) : [ResultDict[key][0], Probability]})
            
            print("\n"+BOLD+"TOTAL:",Sum,"characters\n"+END)
    return ResultDict


#This function calculates the number of occurences and frequency in text of bigrams of letters from CharArray
#  DoublePass = True - runs two passes with offseto of 1 for higher accuracy of bigram frequencies
def CalculateBigramFrequency(InputFileName, CharArray, DoublePass = True):    

    ResultDict = {}
    Sum = 0
    for i in range(0, len(CharArray)):
        for j in range(0, len(AllowedChars)):
            ResultDict.update({AllowedChars[i]+AllowedChars[j]: [0,0]})
    
    if (os.path.isfile(InputFileName)):
        with open(InputFileName, "r", encoding="utf-8") as InputFile:
            for i in range(0,2):
                InputFile.seek(0)
                if (i == 1):
                    InputFile.read(1)
                while True:
                    char = InputFile.read(2).lower()
                    #print(char)
                    if ((len(char) == 2) and (char[0] in CharArray) and (char[1] in CharArray)):
                        ResultDict.update({char: [ResultDict[char][0] + 1,0]})
                        Sum = Sum + 1
                    
                    if(Sum % 10 == 0):
                        print("Processing char № "+YELLOW+BOLD+str(Sum)+END+END, end='\r')
                        
                    if not char:
                        print(YELLOW+BOLD+"Processing of bigrams completed!"+END+END)
                        break
                    
                if (DoublePass == False):
                    break
                
            InputFile.close()
            for key in ResultDict.keys():
                Probability = round(ResultDict[key][0] / Sum, 8)
                ResultDict.update({str(key) : [ResultDict[key][0], Probability]})
            
            print("\n"+BOLD+"TOTAL:",Sum,"bigrams\n"+END)
    return ResultDict


#This function calculates the entropy of n-grams for given occurence frequency dict with structure of { N-gram:[NofOccurences, Frequency] }
def CalculateEntropy(FrequencyDict):
    EntropyOfN = 0
    for key, value in FrequencyDict.items():
        if(value[1] != 0):
            EntropyOfN = EntropyOfN + (value[1] * math.log(value[1], 2))
    
    EntropyOfN = -EntropyOfN / len(next(iter(FrequencyDict)))
    return EntropyOfN


#This function converts the frequency and probability data of bigrams from dict into 2d Pandas dataframe
def FreqencyDict2dToDataframe(FrequencyDict, CharArray, Freq = True):
    if(Freq == False):
        val = 1
        fill = 0.0
    else:
        val = 0
        fill = 0
        
    df = pd.DataFrame(columns = CharArray)
    for i in range(0, len(CharArray)):
        df.loc[len(df)] = [fill]*len(CharArray)
    df.index = CharArray
    
    for key, value in FrequencyDict.items():
        if(value[val] != 0):
            df.at[key[0], key[1]] = value[val]          
    return df


#This function converts frequency and probability data from dict into Pandas dataframe and .CSV file
def FrequencyDictToCSV(OutputFile, FrequencyDictSingleChar, FrequencyDictBigram, FrequencyDictBigramDouble, CharArray):
    pd.set_option("display.precision", 8)
    df11 = FreqencyDict2dToDataframe(FrequencyDictBigram, CharArray, True)
    df12 = FreqencyDict2dToDataframe(FrequencyDictBigram, CharArray, False)
    
    df21 = FreqencyDict2dToDataframe(FrequencyDictBigramDouble, CharArray, True)
    df22 = FreqencyDict2dToDataframe(FrequencyDictBigramDouble, CharArray, False)
    
    df3 = pd.DataFrame(columns = ["Frequency", "Probability"])
    for i in range(0, len(CharArray)):
        df3.loc[len(df3)] = [0, 0.0]
        df3 = df3.astype({"Frequency":"int", "Probability":"float"})
    df3.index = CharArray
    for key, value in FrequencyDictSingleChar.items():
        if(value[1] != 0):
            df3.at[key, "Frequency"] = value[0]
            df3.at[key, "Probability"] = value[1]     
    
    if (OutputFile[-4:] == ".csv"):
        Name = OutputFile[:-4]
    else:
        Name = OutputFile
    
    print(BOLD+"Frequency of bigrams in text (single pass with step = 2):\n"+END,df11,"\n")
    df11.to_csv(Name+"-Bg-Freq-Singlepass.csv")
    print(BOLD+"Probability of bigrams in text (single pass with step = 2):\n"+END,df12,"\n")
    df12.to_csv(Name+"-Bg-Pro-Singlepass.csv")
    print(BOLD+"Frequency of bigrams in text (double pass with overlap):\n"+END,df21,"\n")
    df21.to_csv(Name+"-Bg-Freq-Doublepass.csv")
    print(BOLD+"Probability of bigrams in text (double pass with overlap):\n"+END,df22,"\n")
    df22.to_csv(Name+"-Bg-Pro-Doublepass.csv")
    print(BOLD+"Frequency and probability of single letters in text:\n"+END,df3,"\n")
    df3.to_csv(Name+"-SingleLetters.csv")
    
    

#Driver code:
if (len(sys.argv) == 4):
    source = sys.argv[1]
    workdir = sys.argv[2]
    
    Exit = False
elif(len(sys.argv) != 4 or (sys.argv[0] == "-h")):
    print("Usage: Crypto-lab1.py <source text> <workdir> <count spaces {T/F}>\n")
    Exit = True
    
if (Exit == False):
    print(BOLD+("="*82))
    print("Text processing and letter frequency, probability and entropy calculation program.")
    print(("="*82)+END+"\n")

    if ((os.path.exists(workdir)) and (os.path.isfile(source))):
        
        #AllowedChars = ["а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", "і", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
        AllowedChars = ["а", "б", "в", "г", "д", "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ы", "ь", "э", "ю", "я"]
        if ((sys.argv[3] == "T") or (sys.argv[3] == "t") or (sys.argv[3] == "True") or (sys.argv[3] == "true")):
            AllowedChars.append(" ")
               
        PreprocessText(AllowedChars, source, workdir+"/out.txt", False)
        
        P1 = CalculateSingleLetterFrequency(workdir+"/out.txt", AllowedChars)
        P2 = CalculateBigramFrequency(workdir+"/out.txt", AllowedChars, False)
        P3 = CalculateBigramFrequency(workdir+"/out.txt", AllowedChars, True)

        FrequencyDictToCSV(workdir+"/crypto_results.csv", P1, P2, P3, AllowedChars)
        print(BOLD+"\nEntropies on the symbol of source:\n"+END)
        print("H2(single pass) =",CalculateEntropy(P2))
        print("H2(double pass) =",CalculateEntropy(P3))
        print("H1 =",CalculateEntropy(P1))
        print("\n")

    else:
        print("ERROR! File or directory does not exist!")




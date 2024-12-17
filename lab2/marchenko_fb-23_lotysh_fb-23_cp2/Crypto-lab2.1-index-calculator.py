# Marchenko Rodion Cryptography lab №2.2 Index of Coincidence calculation for Vigenere scipher:

import math
import os.path
import sys
import pandas as pd

BOLD = "\033[1m"
END = "\033[0m"
YELLOW = "\033[1;33m"

Latin = list("abcdefghijklmnopqrstuvwxyz")
Cyrilic1 = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
Cyrilic2 = list("абвгдежзиіїйклмнопрстуфхцчшщьєюя")


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
                    if (char in AllowedChars):
                        if ((char != " ") or (char == " " and FormerChar != " ")): #Multiple spaces in a row prevention
                            OutputFile.write(char)
                            FormerChar = char
                    if not char:
                        break

                OutputFile.close()
                InputFile.close()


#This function calculates the number of occurences and frequency in text of single letters from CharArray
def CalculateSingleLetterFrequencyFromText(InputText, CharArray):

	ResultDict = {}
	Sum = 0
	for i in range(0, len(CharArray)):
		ResultDict.update({CharArray[i]: [0,0]})

	if (len(InputText)!= 0):
		for i in range(0, len(InputText)):
			char = InputText[i].lower()
			if (char in CharArray):
				ResultDict.update({char: [ResultDict[char][0] + 1,0]})
				Sum = Sum + 1

			if(Sum % 10 == 0):
				print("Processing char № "+YELLOW+BOLD+str(Sum)+END+END, end='\r')

		print(YELLOW+BOLD+"Processing of single characters completed!"+END+END, end='\r')

		for key in ResultDict.keys():
			Probability = round(ResultDict[key][0] / Sum, 8)
			ResultDict.update({str(key) : [ResultDict[key][0], Probability]})

		print("\n"+BOLD+"TOTAL:",Sum,"characters\n"+END)
	return ResultDict


#This function prints character frequency results as a pandas dataframe
def PrintFrequencyResults(FrequencyDictSingleChar, CharArray):

	df3 = pd.DataFrame(columns = ["Frequency", "Probability"])
	for i in range(0, len(CharArray)):
		df3.loc[len(df3)] = [0, 0.0]
		df3 = df3.astype({"Frequency":"int", "Probability":"float"})
	df3.index = CharArray
	for key, value in FrequencyDictSingleChar.items():
		if(value[1] != 0):
			df3.at[key, "Frequency"] = value[0]
			df3.at[key, "Probability"] = value[1]

	print(BOLD+"Frequency and probability of single letters in text:\n"+END,df3,"\n")


#This function separates the input text into subtexts of characters, separated by period R (i, i+R, i+2R ...)
def SeparateSubtext(InputText, R):
	SubtextArray = [""]*R
	cnt = 0

	for i in range(0, len(InputText)):
		if (cnt == R):
			cnt = 0
		SubtextArray[cnt] = SubtextArray[cnt] + InputText[i]
		cnt = cnt+1

	return SubtextArray


#This function calculates the index of coincidence I(Y) by a given text length and letter frequencies
def CalculateCoincidenceIndex(FrequencyDictSingleChar, InputTextLen):
	CoincidenceIndexSum = 0
	if (len(FrequencyDictSingleChar) != 0 and InputTextLen > 0):
		for key, value in FrequencyDictSingleChar.items():
			if(value[0] != 0):
				CoincidenceIndexSum = CoincidenceIndexSum + value[0]*(value[0]-1)

		Index = CoincidenceIndexSum / (InputTextLen*(InputTextLen - 1))

	return Index




##### Driver code: #####

if (len(sys.argv) == 5):
	try:
		source = sys.argv[1]
		R = int (sys.argv[2])
		workdir = sys.argv[3]
		alphabet = sys.argv[4]
		Exit = False

	except:
		print("Usage: Crypto-lab1.py <source text> <cipher period (R)> <workdir> <alphabet (EN, RU, UA)>\n")
		Exit = True

elif(len(sys.argv) != 5 or (sys.argv[0] == "-h")):
	print("Usage: Crypto-lab1.py <source text> <cipher period (R)> <workdir> <alphabet (EN, RU, UA)>\n")
	Exit = True

if (Exit == False):
	print("\n╔"+("═"*58)+"╗")
	print("║Viginere scipher Index Of Coincidence calculation program.║")
	print("╚"+("═"*58)+"╝")

	if ((os.path.exists(workdir)) and (os.path.isfile(source))):

		#Choose alphabet
		if (alphabet == "EN" or alphabet == "en"):
			Alfa = Latin
		if (alphabet == "UA" or alphabet == "ua"):
			Alfa = Cyrilic2
		if (alphabet == "RU" or alphabet == "ru"):
			Alfa = Cyrilic1

		#Strip the text of non-alphabet charcters
		PreprocessText(Alfa, source, workdir+"/IndexCalcProcessedText.txt", False)

		with open(workdir+"/IndexCalcProcessedText.txt", "r", encoding="utf-8") as InputFile:
			OriginalText = InputFile.read() #Get input text
			SubtextArray = SeparateSubtext(OriginalText, R) #Get subtexts

			#Find I(Y) for the whole text:
			P1 = CalculateSingleLetterFrequencyFromText(OriginalText, Alfa)
			PrintFrequencyResults(P1, Alfa)
			Itxt = round(CalculateCoincidenceIndex(P1, len(OriginalText)), 8)

			#Find I(Y) for subtexts:
			IndexesArray = [0]*R
			for i in range(0, R):
				PI = CalculateSingleLetterFrequencyFromText(SubtextArray[i], Alfa)
				IndexesArray[i] = round(CalculateCoincidenceIndex(PI, len(SubtextArray[i])), 8)


			#PRINT ANSWER TABLE:#
			print("\n╔" + ("═"*58) + "╗")
			print("║ Indices of Coincidence of the text" + (" "*23) + "║")
			print("║ \"" + source + "\"" + (" "*(55-len(source))) + "║")
			print("║ for Vigenere scipher period R == "+str(R)+":"+(" "*(23-len(str(R))))+"║")
			print("║" + (" "*58) + "║")
			print("║ > Itxt == "+ str(Itxt) + (" "*(47-len(str(Itxt))))+"║")

			for i in range(0, R):
				print("║ > I"+ str(i) + (" "*(3-len(str(i)))) + " == " +  str(IndexesArray[i]) + (" "*(47-len(str(IndexesArray[i])))) + "║")

			print("╚" + ("═"*58) + "╝")
			#####################

			print("\n")

	else:
		print("ERROR! File or directory does not exist!")










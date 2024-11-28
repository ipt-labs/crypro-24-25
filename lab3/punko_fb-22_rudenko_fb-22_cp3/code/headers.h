#pragma once
#include <iostream>
#include <string>
#include <vector>
#include <Windows.h>
#include <map>
#include <algorithm>
#include <cmath>
#include <fstream>

//alphabet without ¸ and ת
static const std::string alphabet = "אבגדהוזחטיךכלםמןנסעףפץצקרשüû‎‏ÿ";
static const int alphabetLength = static_cast<int>(alphabet.size()); 
static const int powedAlphabetLength = static_cast<int>(pow(alphabetLength, 2));

//most frequent bigramms of russian language
static const std::vector<std::string> mostFreqLanguageBigramms = { "סע", "םמ", "עמ", "םא", "ום" };

//most and least frequent letters of russian language
static const std::string mostFreqLettersToCheck = "מואטם", leastFreqLettersToCheck = "פ‎שצ‏";

//read_file.cpp
std::string readFile(const wchar_t* filePath);

//math.cpp
int gcd(int a, int b);
int inverseElement(int a, int alphLen);
std::vector<int> solveLinearCongruence(int a, int b, int n);

//letters_and_bigramms.cpp
std::map<std::string, uint64_t> countBigramms(std::string& text);
std::vector<std::pair<std::string, uint64_t>> bigrammsSortedByFrequency(std::string& text);
std::map<char, uint64_t> countLetters(std::string& text);
std::vector<std::pair<unsigned int, unsigned int>> formPairs(const std::vector<std::string>& bigramms);

//text_analizer.cpp
bool naturalLanguageAnalizer(std::string& text);

//decryption.cpp
std::pair<int, int> guessKey(std::pair<unsigned int, unsigned int> textPairBigramm, std::pair<unsigned int, unsigned int> langPairBigramm);
std::vector<std::pair<int, int>> guessAllKeys(const std::vector<std::string>& topTextBigramms);
std::string decrypt(const std::string& cryptedText, const std::pair<int, int>& key, const std::string& alphabet);
void decryptAndSave(const std::vector<std::pair<int, int>>& potentialKeys, std::string& text, int& written);
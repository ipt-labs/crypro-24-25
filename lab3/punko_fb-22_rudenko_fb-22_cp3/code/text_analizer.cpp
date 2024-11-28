#include "headers.h"

bool naturalLanguageAnalizer(std::string& text) {
    std::map<char, uint64_t> letterCount = countLetters(text);
    std::vector<char> mostFreqLetters, leastFreqLetters;

    for (const auto& pair : letterCount) mostFreqLetters.push_back(pair.first);

    std::sort(mostFreqLetters.begin(), mostFreqLetters.end(), [&letterCount](char a, char b) {
        return letterCount[a] > letterCount[b];
        });

    leastFreqLetters = mostFreqLetters;
    std::reverse(leastFreqLetters.begin(), leastFreqLetters.end());

    if (mostFreqLetters.size() > 5) {
        mostFreqLetters.resize(5);
        leastFreqLetters.resize(5);
    }

    uint8_t mostFreqHit = 0, leastFreqHit = 0;

    for (int i = 0; i < 5; i++) {
        if (mostFreqLettersToCheck.find(mostFreqLetters[i]) != std::string::npos) mostFreqHit++;
        if (leastFreqLettersToCheck.find(leastFreqLetters[i]) != std::string::npos) leastFreqHit++;
    }

    if (mostFreqHit < 3 || leastFreqHit < 1) return false;

    std::map<std::string, uint64_t> bigrammsCount = countBigramms(text);
    std::vector<std::string> mostFreqBigramms;

    for (const auto& pair : bigrammsCount) mostFreqBigramms.push_back(pair.first);

    std::sort(mostFreqBigramms.begin(), mostFreqBigramms.end(), [&bigrammsCount](const std::string& a, const std::string& b) {
        return bigrammsCount[a] > bigrammsCount[b];
        });

    if (mostFreqBigramms.size() > 5) mostFreqBigramms.resize(5);

    uint8_t bigrammsHit = 0;
    for (const std::string& bigramm : mostFreqBigramms) {
        if (std::find(mostFreqLanguageBigramms.begin(), mostFreqLanguageBigramms.end(), bigramm) != mostFreqLanguageBigramms.end()) bigrammsHit++;
    }
    return bigrammsHit >= 3;
}
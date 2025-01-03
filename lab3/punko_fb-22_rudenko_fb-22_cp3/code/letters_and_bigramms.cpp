#include "headers.h"

std::map<std::string, uint64_t> countBigramms(std::string& text) {
    std::map<std::string, uint64_t> dictionary_bigramm;
    for (char first : alphabet) {
        for (char second : alphabet) {
            std::string bigram = { first, second };
            dictionary_bigramm[bigram] = 0;
        }
    }

    uint64_t bigramm_count = 0;
    bigramm_count = text.size() / 2;
    for (uint64_t i = 0; i < text.size() - 1; i += 2) {
        std::string bigramm = text.substr(i, 2);
        dictionary_bigramm[bigramm]++;
    }

    return dictionary_bigramm;
}

std::vector<std::pair<std::string, uint64_t>> bigrammsSortedByFrequency(std::string& text) {
    std::map<std::string, uint64_t> bigramms = countBigramms(text);
    std::vector<std::pair<std::string, uint64_t>> bigrammsVector(bigramms.begin(), bigramms.end());

    std::sort(bigrammsVector.begin(), bigrammsVector.end(),
        [](const std::pair<std::string, uint64_t>& a, const std::pair<std::string, uint64_t>& b) {
            return a.second > b.second;
        });

    return bigrammsVector;
}

std::map<char, uint64_t> countLetters(std::string& text) {
    std::map<char, uint64_t> letters;
    for (char ch : text) {
        letters[ch]++;
    }
    return letters;
}

std::vector<std::pair<unsigned int, unsigned int>> formPairs(const std::vector<std::string>& bigramms) {
    std::vector<std::pair<unsigned int, unsigned int>> pairs;
    for (int i = 0; i < bigramms.size(); i++) {
        for (int j = i + 1; j < bigramms.size(); j++) {

            unsigned int firstCharIndex = alphabet.find(bigramms[i][0]);
            unsigned int secondCharIndex = alphabet.find(bigramms[i][1]);
            unsigned int firstBigramm = (firstCharIndex * alphabet.length()) + secondCharIndex;

            unsigned int thirdCharIndex = alphabet.find(bigramms[j][0]);
            unsigned int fourthCharIndex = alphabet.find(bigramms[j][1]);
            unsigned int secondBigramm = (thirdCharIndex * alphabet.length()) + fourthCharIndex;

            pairs.push_back({ firstBigramm, secondBigramm });
        }
    }
    return pairs;
}
#include "headers.h"

std::pair<int, int> guessKey(std::pair<unsigned int, unsigned int> textPairBigramm, std::pair<unsigned int, unsigned int> langPairBigramm) {
    int x = static_cast<int>(langPairBigramm.first) - static_cast<int>(langPairBigramm.second) % powedAlphabetLength;
    int y = static_cast<int>(textPairBigramm.first) - static_cast<int>(textPairBigramm.second) % powedAlphabetLength;
    std::vector<int> a = solveLinearCongruence(x, y, powedAlphabetLength);
    if (!a.empty()) {
        int b = (static_cast<int>(textPairBigramm.first) - a[0] * static_cast<int>(langPairBigramm.first)) % powedAlphabetLength;
        while (b < 0) b += powedAlphabetLength;
        while (a[0] < 0) a[0] += powedAlphabetLength;
        return std::make_pair(a[0], b);
    }

    return std::make_pair(-1, -1);
}

std::vector<std::pair<int, int>> guessAllKeys(const std::vector<std::string>& topTextBigramms) {
    auto textPairBigramms = formPairs(topTextBigramms);
    auto langPairBigramms = formPairs(mostFreqLanguageBigramms);

    std::vector<std::pair<int, int>> potentialKeys;

    for (auto textPair : textPairBigramms) {
        for (auto langPair : langPairBigramms) {
            std::pair<int, int> key = guessKey(textPair, langPair);
            if (key.first != -1) potentialKeys.push_back(key);
        }
    }

    std::sort(potentialKeys.begin(), potentialKeys.end());
    potentialKeys.erase(std::unique(potentialKeys.begin(), potentialKeys.end()), potentialKeys.end());

    return potentialKeys;
}


std::string decrypt(const std::string& cryptedText, const std::pair<int, int>& key, const std::string& alphabet) {
    int aInverted = inverseElement(key.first, powedAlphabetLength);

    std::vector<int> textAsNums(cryptedText.size() / 2, 0);

    for (size_t i = 0; i < cryptedText.size() / 2; i++) {
        int firstChar = alphabet.find(cryptedText[i * 2]);
        int secondChar = alphabet.find(cryptedText[i * 2 + 1]);
        textAsNums[i] = firstChar * alphabetLength + secondChar;
    }

    std::vector<int> decryptedNums(textAsNums.size());
    for (size_t i = 0; i < textAsNums.size(); i++) {
        int decryptedNum = (aInverted * (textAsNums[i] - key.second)) % powedAlphabetLength;
        while (decryptedNum < 0) decryptedNum += powedAlphabetLength;
        decryptedNums[i] = decryptedNum;
    }

    std::string decrypted;
    for (int num : decryptedNums) {
        int firstChar = num / alphabetLength;
        int secondChar = num % alphabetLength;
        decrypted += alphabet[firstChar];
        decrypted += alphabet[secondChar];
    }

    return decrypted;
}

void decryptAndSave(const std::vector<std::pair<int, int>>& potentialKeys, std::string& text, int& written) {
    std::ofstream outFile(L"decrypted_texts.txt");
    if (!outFile) {
        std::wcerr << L"Cannot create file \"decrypted_texts.txt\" for write.\n";
        return;
    }

    for (const auto& key : potentialKeys) {
        int aInverted = inverseElement(key.first, static_cast<int>(std::pow(alphabet.size(), 2)));
        if (aInverted == -1) continue;

        std::string decryptedText = decrypt(text, key, alphabet);
        if (naturalLanguageAnalizer(decryptedText)) {
            outFile << "Key: (" << key.first << ", " << key.second << ")\n";
            outFile << decryptedText << "\n\n";
            std::wcout << L"Text has been decrypted: with key (" << key.first << L", " << key.second
                << L") and been written in: \"decrypted_texts.txt\"\n";
            written++;
        }
    }

    outFile.close();
}
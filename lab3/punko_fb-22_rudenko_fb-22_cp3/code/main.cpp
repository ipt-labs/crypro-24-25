#include "headers.h"

int wmain(int argc, wchar_t* argv[]) {
    _wsetlocale(LC_ALL, L"ru-RU");

    if (argc < 2) {
        std::wcerr << L"Usage: " << argv[0] << L" <path to file>\n";
        return 1;
    }

    std::wstring filePath = argv[1];
    std::string text = readFile(argv[1]);

    if (text == "") return 1;

    auto mostFreqTextBigramms = bigrammsSortedByFrequency(text);
    std::vector<std::string> topTextBigramms;

    std::wcout << L"5 most frequent bigramms:\n";
    for (int i = 0; i < 5 && i < mostFreqTextBigramms.size(); ++i) {
        std::cout << mostFreqTextBigramms[i].first << ":\t" << mostFreqTextBigramms[i].second << '\n';
        topTextBigramms.push_back(mostFreqTextBigramms[i].first);
    }
    std::wcout << L'\n';

    auto potentialKeys = guessAllKeys(topTextBigramms);

    int written = 0;
    decryptAndSave(potentialKeys, text, written);
    if (written > 0) std::wcout << "Possible texts: " << written << '\n';
    else std::wcout << "There is no possible decryption\n";

    return 0;
}

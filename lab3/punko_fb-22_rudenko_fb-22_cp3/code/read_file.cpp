#include "headers.h"

std::string readFile(const wchar_t* filePath) {
    std::ifstream file(filePath, std::ios::binary);
    if (!file.is_open()) {
        std::wcerr << L"Cannot open the \"" << filePath << L"\" file\n";
        return {};
    }

    std::string text;
    char c;
    while (file.get(c)) {
        if (c != '\n' && c != '\r') {
            text += c;
        }
    }

    if (file.bad()) {
        std::wcerr << L"Error while reading: \"" << filePath << L"\" file\n";
        return {};
    }

    return text;
}

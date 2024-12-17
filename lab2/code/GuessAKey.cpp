#include "MyForm.h"

std::map<size_t, double> calculateIC(const std::string& text) {
    std::map<size_t, double> indices;
    size_t len = text.length();

    for (int i = 2; i <= 64; i++) {
        std::vector<std::string> groups(i);
        for (size_t j = 0; j < len; j++) {
            groups[j % i] += text[j];
        }

        double avgIC = 0.0;
        for (const std::string& group : groups) {
            std::map<char, int> freq;
            for (char ch : group) {
                freq[ch]++;
            }

            size_t len = group.length();
            if (len <= 1) continue;
            double IC = 0.0;
            for (const auto& pair : freq) {
                IC += pair.second * (pair.second - 1.0);
            }
            IC /= (len * (len - 1.0));
            avgIC += IC;
        }
        avgIC /= i;
        indices[i] = avgIC;
    }

    return indices;
}

std::string possibleKey(const std::string& text, unsigned long keyLen) {
    std::string key = "";
    size_t len = text.length();

    std::vector<std::string> groups(keyLen);
    for (size_t i = 0; i < len; i++) {
        groups[i % keyLen] += text[i];
    }

    for (const auto& group : groups) {
        std::map<char, int> freq;
        for (const char& c : group) {
            freq[c]++;
        }

        char mostFreqLetter = std::max_element( freq.begin(), freq.end(), 
            [](const auto& a, const auto& b) { return a.second < b.second; }
        )->first;

        int shift = (mostFreqLetter - 238 + 32) % 32;
        if (shift < 0) shift += 32;
        key += static_cast<char>(224 + shift);
    }
    return key;
}

void Cryptalaba2::MyForm::GuessAKey(System::Object^ sender, System::EventArgs^ e) {
    std::filesystem::path filePath = msclr::interop::marshal_as<std::wstring>(this->PathToFileTextBox->Text);
    HANDLE hFile = CreateFileW(filePath.c_str(), GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        MessageBox::Show("File does not exist");
        return;
    }

    LARGE_INTEGER fileSize = { 0 };
    if (!GetFileSizeEx(hFile, &fileSize)) {
        MessageBox::Show("Cannot get file size");
        CloseHandle(hFile);
        return;
    }

    char* buffer = new char[fileSize.QuadPart];
    DWORD bytesRead = 0;
    if (!ReadFile(hFile, buffer, static_cast<DWORD>(fileSize.QuadPart), &bytesRead, NULL)) {
        MessageBox::Show("Cannot read the file");
        delete[] buffer;
        CloseHandle(hFile);
        return;
    }
    CloseHandle(hFile);

    std::string filteredText = "";
    for (int i = 0; i < bytesRead; i++) {
        if (static_cast<unsigned char>(buffer[i]) >= 224 && static_cast<unsigned char>(buffer[i]) <= 255) filteredText += buffer[i];
    }
    delete[] buffer;

    if (filteredText.empty()) {
        MessageBox::Show("Please enter file with little russian letters");
        return;
    }

    std::map<size_t, double> indices = calculateIC(filteredText);

    size_t mostProbableLen = 2;
    double maxIC = indices.at(mostProbableLen);

    for (const auto& index : indices) {
        if (index.second > maxIC) {
            maxIC = index.second;
            mostProbableLen = index.first;
        }
    }

    std::string key = possibleKey(filteredText, mostProbableLen);

    std::filesystem::path directory = filePath.parent_path();
    std::wstring fileName = filePath.stem().wstring() + L"_analize.txt";
    std::filesystem::path newFilePath = directory / fileName;
    std::wstring fullPath = newFilePath.wstring();

    hFile = CreateFileW(fullPath.c_str(), GENERIC_WRITE, NULL, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        MessageBox::Show("Cannot create file");
        CloseHandle(hFile);
        return;
    }

    std::string resultString = "ANALIZE RESULT:\n---------------------------------------\n\nINDECES COINCIDENCE:\n\n";
    for (const auto& index : indices) {
        resultString += std::to_string(index.first) + ": " + std::to_string(index.second) + "\n";
    }
    resultString += "\nThe most possible key length: " + std::to_string(mostProbableLen) + "\nThe most possible key: " + key;

    DWORD bytesWritten = 0;
    if (!WriteFile(hFile, resultString.c_str(), resultString.length(), &bytesWritten, NULL)) {
        MessageBox::Show("Cannot write analize to file");
    }

    CloseHandle(hFile);
}
#include "MyForm.h"

void Cryptalaba2::MyForm::Crypt(bool decrypt) {
    if (System::String::IsNullOrEmpty(this->KeyTextBox->Text)) {
        MessageBox::Show("Enter the key");
        return;
    }

    std::string key = msclr::interop::marshal_as<std::string>(this->KeyTextBox->Text);

    if (key.empty()) {
        MessageBox::Show("Enter the key");
        return;
    }

    for (char c : key) {
        if (!(c >= 'à' && c <= 'ÿ')) {
            MessageBox::Show("Enter key in russian alphabet (without ¸)");
            return;
        }
    }

    std::filesystem::path filePath = msclr::interop::marshal_as<std::wstring>(this->PathToFileTextBox->Text);
    HANDLE hFile = CreateFileW(filePath.c_str(), GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE,
        NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        MessageBox::Show("File does not exist");
        return;
    }

    LARGE_INTEGER fileSize = { 0 };
    if (!GetFileSizeEx(hFile, &fileSize)) {
        MessageBox::Show("Cannot get file size");
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

    std::string result(fileSize.QuadPart, 0);

    for (size_t i = 0; i < bytesRead; i++) {
        if (buffer[i] >= 'à' && buffer[i] <= 'ÿ') {
            int charIndex = buffer[i] - 'à';
            int shift = key[i % key.size()] - 'à';
            int newIndex;

            if (decrypt) {
                newIndex = (charIndex - shift + 32) % 32;
            }
            else {
                newIndex = (charIndex + shift) % 32;
            }

            result[i] = 'à' + newIndex;
        }
        else {
            result[i] = buffer[i];
        }
    }

    std::map<char, int> freq;
    int totalAlphabetChars = 0;

    for (size_t i = 0; i < result.size(); i++) {
        if (result[i] >= 'à' && result[i] <= 'ÿ') {
            freq[result[i]]++;
            totalAlphabetChars++;
        }
    }

    if (totalAlphabetChars < 2) {
        this->CoincidenceIndicesLabel->Text = "Coincidence Index: 0";
    }
    else {
        double indexCoincidence = 0.0;
        for (const auto& pair : freq) {
            indexCoincidence += (pair.second * (pair.second - 1.0));
        }
        indexCoincidence /= (totalAlphabetChars * (totalAlphabetChars - 1.0));

        this->CoincidenceIndicesLabel->Text = "Coincidence Index: " +
            System::Convert::ToString(System::Math::Round(indexCoincidence, 4));
    }
    
    delete[] buffer;
    CloseHandle(hFile);

    std::wstring fileName = filePath.stem().wstring();
    std::wstring extension = filePath.extension().wstring();
    std::wstring suffix = decrypt ? L"_decrypted" : L"_crypted";
    std::wstring newFileName = fileName + suffix + extension;
    std::filesystem::path newFilePath = filePath.parent_path() / newFileName;

    hFile = CreateFileW(newFilePath.c_str(), GENERIC_WRITE, NULL, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        MessageBox::Show("Cannot create file");
        return;
    }

    DWORD bytesWritten = 0;
    if (!WriteFile(hFile, result.c_str(), bytesRead, &bytesWritten, NULL)) {
        MessageBox::Show("Cannot write to file");
    }

    MessageBox::Show(decrypt ? "File has been decrypted" : "File has been encrypted");
    CloseHandle(hFile);
}
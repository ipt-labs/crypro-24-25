#include "MyForm.h"

void cryptolab1::MyForm::CountLetter_Click(System::Object^ sender, System::EventArgs^ e) {
    std::map<char, uint64_t> dictionary;

    std::wstring filepath = msclr::interop::marshal_as<std::wstring>(this->pathToFile_box->Text);
    HANDLE hFile = CreateFileW(filepath.c_str(), GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        if (this->pathToFile_box->Text == initial_pathTextbox_text) MessageBox::Show("Enter a file");
        else MessageBox::Show("Error while opening: " + this->pathToFile_box->Text);
        return;
    }

    LARGE_INTEGER fileSize = { 0 };
    GetFileSizeEx(hFile, &fileSize);

    char* buffer = new char[fileSize.QuadPart + 1];
    DWORD bytesRead = 0;
    if (!ReadFile(hFile, buffer, fileSize.QuadPart, &bytesRead, NULL)) {
        MessageBox::Show("Error while reading: " + this->pathToFile_box->Text);
        delete[] buffer;
        CloseHandle(hFile);
        return;
    }
    buffer[bytesRead] = '\0';
    CloseHandle(hFile);

    for (uint64_t i = 0; i < bytesRead; i++) {
        dictionary[buffer[i]]++;
    }
    delete[] buffer;

    libxl::Book* book = xlCreateBook();
    if (!book) {
        MessageBox::Show("Error while creating book");
        return;
    }
    libxl::Sheet* sheet = book->addSheet(L"Letter frequencies");
    if (!sheet) {
        MessageBox::Show("Error while creating sheet");
        return;
    }

    String^ result = "";
    double entropy = 0.0f;
    unsigned int row = 0;

    for (const auto& pair : dictionary) {
        double frequency = static_cast<double>(pair.second) / bytesRead;
        entropy += frequency * log2(frequency);

        result += String::Format("Letter: '{0}'{1}Count: {2}{1}Frequency: {3:F10}{1}", gcnew String(&pair.first, 0, 1),
            Environment::NewLine, pair.second, frequency);

        wchar_t unicode_char = { 0 };
        char temp[2] = { pair.first, '\0' };
        MultiByteToWideChar(1251, 0, temp, -1, &unicode_char, 1);

        sheet->writeStr(row, 0, &unicode_char);
        sheet->writeNum(row, 1, pair.second);
        sheet->writeNum(row, 2, frequency);
        row++;
    }
    entropy *= -1;

    std::wstring::size_type last_dot = filepath.find_last_of(L'.');
    filepath = filepath.substr(0, last_dot);
    std::wstring file_name = filepath.substr(0, last_dot) + L"_letters_freq_table.xls";

    uint16_t unique_chars = 0;
    for (const auto& pair : dictionary) {
        if (pair.second > 0) unique_chars++;
    }

    double redundancy = 1 - (entropy / log2(static_cast<double>(unique_chars)));

    sheet->writeStr(row, 0, L"Entropy");
    sheet->writeNum(row, 1, entropy);
    sheet->writeStr(row, 2, L"Redundancy");
    sheet->writeNum(row, 3, redundancy);
    book->save(file_name.c_str());
    book->release();

    this->Result_box->Text = result;
    this->enthropy_textbox->Text = "Entropy: " + entropy.ToString() + "\tRedundancy: " + redundancy.ToString();
}
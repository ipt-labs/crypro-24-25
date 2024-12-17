#include "MyForm.h"

void cryptolab1::MyForm::CountBigramm_Click(System::Object^ sender, System::EventArgs^ e) {
    System::Windows::Forms::Button^ clickedButton = dynamic_cast<System::Windows::Forms::Button^>(sender);
    String^ mode = dynamic_cast<String^>(clickedButton->Tag);
    std::map<std::string, uint64_t> dictionary_bigramm;
    const std::string alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ";

    for (char first : alphabet) {
        for (char second : alphabet) {
            std::string bigram = { first, second };
            dictionary_bigramm[bigram] = 0;
        }
    }

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

    uint64_t bigramm_count = 0;

    if (mode == "overlapped") {
        bigramm_count = bytesRead - 1;
        for (uint64_t i = 0; i < bytesRead - 1; i++) {
            std::string bigramm(buffer + i, 2);
            dictionary_bigramm[bigramm]++;
        }
    }
    else {
        bigramm_count = bytesRead / 2;
        for (uint64_t i = 0; i < bytesRead - 1; i += 2) {
            std::string bigramm(buffer + i, 2);
            dictionary_bigramm[bigramm]++;
        }
    }
    delete[] buffer;

    libxl::Book* book = xlCreateBook();
    if (!book) {
        MessageBox::Show("Error while creating book");
        return;
    }
    libxl::Sheet* sheet = book->addSheet(L"Bigramm Frequencies");
    if (!sheet) {
        MessageBox::Show("Error while creating sheet");
        return;
    }

    String^ result = "";
    double entropy = 0.0f;
    unsigned row = 2;
    auto it = dictionary_bigramm.begin();
    auto end = dictionary_bigramm.end();

    if (it != end) {
        char prevLetter = it->first[0];

        while (it != end) {
            int column = 1;
            wchar_t unicode_char = { 0 };
            char temp[2] = { prevLetter, '\0' };
            MultiByteToWideChar(1251, 0, temp, -1, &unicode_char, 1);
            sheet->writeStr(row, 0, &unicode_char);

            while (it != end && prevLetter == it->first[0]) {
                const auto& pair = *it;

                double frequency = static_cast<double>(pair.second) / bigramm_count;
                if (frequency > 0.0f) {
                    entropy += frequency * log2(frequency);
                }

                result += String::Format("Bigramm: '{0}'{1}Count: {2}{1}Frequency: {3:F10}{1}",
                    gcnew String(pair.first.c_str()), Environment::NewLine, pair.second, frequency);

                wchar_t unicode_char_inner = { 0 };
                char temp_inner[2] = { pair.first[1], '\0' };
                MultiByteToWideChar(1251, 0, temp_inner, -1, &unicode_char_inner, 1);

                sheet->writeStr(1, column, &unicode_char_inner);
                sheet->writeNum(row, column, frequency);

                column++;
                it++;
            }

            row++;
            if (it != end) {
                prevLetter = it->first[0];
            }
        }
    }
    entropy *= -1;
    entropy /= 2;

    std::wstring::size_type last_dot = filepath.find_last_of(L'.');
    filepath = filepath.substr(0, last_dot);
    std::wstring mode_str = msclr::interop::marshal_as<std::wstring>(mode);
    std::wstring file_name = filepath.substr(0, last_dot) + L'_' + mode_str + L"_bigramm_freq_table.xls";

    std::set<char> unique_chars_set;
    for (const auto& pair : dictionary_bigramm) {
        if (pair.second > 0) {
        unique_chars_set.insert(pair.first[0]);
        unique_chars_set.insert(pair.first[1]);
        }
    }
    uint16_t unique_chars = static_cast<uint16_t>(unique_chars_set.size());

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

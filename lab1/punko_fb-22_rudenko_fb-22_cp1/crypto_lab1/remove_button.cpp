#include "MyForm.h"

unsigned char toLowerCP1251(unsigned char ch) {
	if (ch >= 192 && ch <= 223) {
		return ch + 32;
	}
	else if (ch == 168) return 184;

	return ch;
}

void cryptolab1::MyForm::Remove_NoneRussian_Click(System::Object^ sender, System::EventArgs^ e) {
	Button^ clickedButton = dynamic_cast<Button^>(sender);
	String^ mode = dynamic_cast<String^>(clickedButton->Tag);
	
	std::wstring filepath = msclr::interop::marshal_as<std::wstring>(this->pathToFile_box->Text);
	HANDLE hFile = CreateFileW(filepath.c_str(), GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hFile == INVALID_HANDLE_VALUE) {
		if (this->pathToFile_box->Text == initial_pathTextbox_text) MessageBox::Show("Enter a file");
		else MessageBox::Show("Error while opening" + this->pathToFile_box->Text);
		return;
	}

	LARGE_INTEGER fileSize = { 0 };
	GetFileSizeEx(hFile, &fileSize);

	char* buffer = new char[fileSize.QuadPart + 1];
	DWORD bytesRead = 0;
	if (!ReadFile(hFile, buffer, fileSize.QuadPart, &bytesRead, NULL)) {
		MessageBox::Show("Error while opening" + this->pathToFile_box->Text);
		delete[] buffer;
		CloseHandle(hFile);
		return;
	}
	buffer[bytesRead] = '\0';
	CloseHandle(hFile);

	char* buffer_for_clean_text = new char[fileSize.QuadPart + 1];
	uint64_t counter = 0;
	bool isSpace = false;
	if (mode == "with_spaces") {
		for (uint64_t i = 0; i < bytesRead; i++) {
			unsigned char ch = static_cast<unsigned char>(buffer[i]);
			if ((ch >= 0xC0 && ch <= 0xFF) ||
				(ch >= 0xA8 && ch <= 0xAF) ||
				 ch == 0xB8) {
				buffer_for_clean_text[counter] = toLowerCP1251(buffer[i]);
				isSpace = false;
				counter++;
			}
			else if (ch == ' ' && !isSpace) { 
				buffer_for_clean_text[counter] = buffer[i];
				isSpace = true;
				counter++;
			}	
		}
	}
	else {
		for (uint64_t i = 0; i < bytesRead; i++) {
			unsigned char ch = static_cast<unsigned char>(buffer[i]);
			if ((ch >= 0xC0 && ch <= 0xFF) ||
				(ch >= 0xA8 && ch <= 0xAF) ||
				ch == 0xB8) {
				buffer_for_clean_text[counter] = toLowerCP1251(buffer[i]);
				counter++;
			}
		}
	}
	delete[] buffer;

	std::wstring::size_type last_dot = filepath.find_last_of(L'.');
	filepath = filepath.substr(0, last_dot);
	std::wstring mode_str = msclr::interop::marshal_as<std::wstring>(mode);

	std::wstring file_name = filepath.substr(0, last_dot) + L"_" + mode_str + L".txt";
	HANDLE hNewFile = CreateFileW(file_name.c_str(), GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hNewFile == INVALID_HANDLE_VALUE) {
		DWORD dwError = GetLastError();
		MessageBox::Show("Error creating file. Error code: " + dwError);
		delete[] buffer_for_clean_text;
		return;
	}

	DWORD bytesWritten = 0;
	if (!WriteFile(hNewFile, buffer_for_clean_text, counter, &bytesWritten, NULL)) {
		DWORD dwError = GetLastError();
		MessageBox::Show("Error writing to file. Error code: " + dwError);
	}

	CloseHandle(hNewFile);
	delete[] buffer_for_clean_text;
}

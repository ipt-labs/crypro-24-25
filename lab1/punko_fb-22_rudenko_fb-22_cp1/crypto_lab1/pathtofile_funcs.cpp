#include "MyForm.h"

void cryptolab1::MyForm::ShowPlaceholder()
{
	if (String::IsNullOrWhiteSpace(pathToFile_box->Text))
	{
		pathToFile_box->Text = initial_pathTextbox_text;
		pathToFile_box->ForeColor = Color::Gray;
	}
}

void cryptolab1::MyForm::HidePlaceholder()
{
	if (pathToFile_box->Text == initial_pathTextbox_text)
	{
		pathToFile_box->Text = String::Empty;
		pathToFile_box->ForeColor = Color::Black;
	}
}

void cryptolab1::MyForm::pathToFile_box_GotFocus(Object^ sender, EventArgs^ e)
{
	HidePlaceholder();
}

void cryptolab1::MyForm::pathToFile_box_LostFocus(Object^ sender, EventArgs^ e)
{
	ShowPlaceholder();
}

void cryptolab1::MyForm::pathToFile_DoubleClick(System::Object^ sender, System::EventArgs^ e) {
	OpenFileDialog^ openFileDialog = gcnew OpenFileDialog();

	openFileDialog->InitialDirectory = "C:\\";
	openFileDialog->RestoreDirectory = true;

	if (openFileDialog->ShowDialog() == System::Windows::Forms::DialogResult::OK) {
		pathToFile_box->Text = openFileDialog->FileName;
	}
}
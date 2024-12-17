#pragma once
#include <Windows.h>
#include <filesystem> 
#include <msclr/marshal_cppstd.h>
#include <map>

namespace Cryptalaba2 {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

	public ref class MyForm : public System::Windows::Forms::Form
	{
	public:
		MyForm(void)
		{
			InitializeComponent();
		}

	protected:
		~MyForm()
		{
			if (components)
			{
				delete components;
			}
		}
	private: 
		System::Windows::Forms::TextBox^ PathToFileTextBox;
		System::Windows::Forms::TextBox^ KeyTextBox;
		System::Windows::Forms::Button^ EncryptButton;
		System::Windows::Forms::Button^ DecryptButton;
		System::Windows::Forms::Button^ KeyLenButton;
		System::Windows::Forms::Label^ CoincidenceIndicesLabel;
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code

		void InitializeComponent(void)
		{
			this->PathToFileTextBox = (gcnew System::Windows::Forms::TextBox());
			this->KeyTextBox = (gcnew System::Windows::Forms::TextBox());
			this->EncryptButton = (gcnew System::Windows::Forms::Button());
			this->DecryptButton = (gcnew System::Windows::Forms::Button());
			this->CoincidenceIndicesLabel = (gcnew System::Windows::Forms::Label());
			this->KeyLenButton = (gcnew System::Windows::Forms::Button());
			this->SuspendLayout();
			// 
			// PathToFileTextBox
			// 
			this->PathToFileTextBox->Location = System::Drawing::Point(12, 12);
			this->PathToFileTextBox->Name = L"PathToFileTextBox";
			this->PathToFileTextBox->Size = System::Drawing::Size(420, 20);
			this->PathToFileTextBox->TabIndex = 0;
			// 
			// KeyTextBox
			// 
			this->KeyTextBox->Location = System::Drawing::Point(12, 38);
			this->KeyTextBox->MaxLength = 64;
			this->KeyTextBox->Name = L"KeyTextBox";
			this->KeyTextBox->Size = System::Drawing::Size(420, 20);
			this->KeyTextBox->TabIndex = 1;
			// 
			// EncryptButton
			// 
			this->EncryptButton->Location = System::Drawing::Point(12, 96);
			this->EncryptButton->Name = L"EncryptButton";
			this->EncryptButton->Size = System::Drawing::Size(140, 24);
			this->EncryptButton->TabIndex = 2;
			this->EncryptButton->Text = L"Encrypt";
			this->EncryptButton->UseVisualStyleBackColor = true;
			this->EncryptButton->Click += gcnew System::EventHandler(this, &MyForm::OnEncryptButtonClick);
			// 
			// DecryptButton
			// 
			this->DecryptButton->Location = System::Drawing::Point(152, 96);
			this->DecryptButton->Name = L"DecryptButton";
			this->DecryptButton->Size = System::Drawing::Size(140, 24);
			this->DecryptButton->TabIndex = 3;
			this->DecryptButton->Text = L"Decrypt";
			this->DecryptButton->UseVisualStyleBackColor = true;
			this->DecryptButton->Click += gcnew System::EventHandler(this, &MyForm::OnDecryptButtonClick);
			// 
			// CoincidenceIndicesLabel
			// 
			this->CoincidenceIndicesLabel->AutoSize = true;
			this->CoincidenceIndicesLabel->Location = System::Drawing::Point(12, 71);
			this->CoincidenceIndicesLabel->Name = L"CoincidenceIndicesLabel";
			this->CoincidenceIndicesLabel->Size = System::Drawing::Size(98, 13);
			this->CoincidenceIndicesLabel->TabIndex = 4;
			this->CoincidenceIndicesLabel->Text = L"Coincidence Index:";
			// 
			// KeyLenButton
			// 
			this->KeyLenButton->Location = System::Drawing::Point(292, 96);
			this->KeyLenButton->Name = L"KeyLenButton";
			this->KeyLenButton->Size = System::Drawing::Size(140, 24);
			this->KeyLenButton->TabIndex = 5;
			this->KeyLenButton->Text = L"Guess a key";
			this->KeyLenButton->UseVisualStyleBackColor = true;
			this->KeyLenButton->Click += gcnew System::EventHandler(this, &MyForm::GuessAKey);
			// 
			// Window
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(444, 132);
			this->Controls->Add(this->KeyLenButton);
			this->Controls->Add(this->CoincidenceIndicesLabel);
			this->Controls->Add(this->DecryptButton);
			this->Controls->Add(this->EncryptButton);
			this->Controls->Add(this->KeyTextBox);
			this->Controls->Add(this->PathToFileTextBox);
			this->FormBorderStyle = System::Windows::Forms::FormBorderStyle::FixedSingle;
			this->MaximizeBox = false;
			this->Name = L"MyForm";
			this->Text = L"Crypto Lab 2";
			this->ResumeLayout(false);
			this->PerformLayout();
		}
#pragma endregion
		void OnEncryptButtonClick(System::Object^ sender, System::EventArgs^ e) {
			Crypt(false);  
		}

		void OnDecryptButtonClick(System::Object^ sender, System::EventArgs^ e) {
			Crypt(true);
		}

		void Crypt(bool decrypt);
		void GuessAKey(System::Object^ sender, System::EventArgs^ e);
	};
}

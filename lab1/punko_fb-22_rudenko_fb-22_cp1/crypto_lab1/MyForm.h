#pragma once
#include <Windows.h>
#include <msclr/marshal_cppstd.h>
#include <string>
#include <vector>
#include <map>
#include <set>
#include "libxl.h"

namespace cryptolab1 {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace System::IO;
	

	/// <summary>
	/// —водка дл€ MyForm
	/// </summary>
	public ref class MyForm : public System::Windows::Forms::Form
	{
	public:
		MyForm(void)
		{
			InitializeComponent();
			this->pathToFile_box->GotFocus += gcnew EventHandler(this, &MyForm::pathToFile_box_GotFocus);
			this->pathToFile_box->LostFocus += gcnew EventHandler(this, &MyForm::pathToFile_box_LostFocus);
			this->pathToFile_box->DoubleClick += gcnew System::EventHandler(this, &MyForm::pathToFile_DoubleClick);
			ShowPlaceholder();
		}

	protected:
		/// <summary>
		/// ќсвободить все используемые ресурсы.
		/// </summary>
		~MyForm()
		{
			if (components)
			{
				delete components;
			}
		}
	private: 
		/// <summary>
		/// ќб€зательна€ переменна€ конструктора.
		/// </summary>
		/// Components
		System::ComponentModel::Container ^components;
		System::Windows::Forms::TextBox^ pathToFile_box;
	    System::Windows::Forms::TextBox^ enthropy_textbox;
	    System::Windows::Forms::Button^ Remove_NoneRussian_without_spaces;
        System::Windows::Forms::Button^ Remove_NoneRussian_with_spaces;
	    System::Windows::Forms::TextBox^ Result_box;
        System::Windows::Forms::Button^ CountLetter_button;
	    System::Windows::Forms::Button^ bigramm_overlapped;
        System::Windows::Forms::Button^ bigramm_not_overlapped;
		System::Windows::Forms::Label^ label1;

		/// Variables
		System::String^ initial_pathTextbox_text = "Enter a path to file...";
		System::String^ entropy_text = "Entropy here";

#pragma region Windows Form Designer generated code
		/// <summary>
		/// “ребуемый метод дл€ поддержки конструктора Ч не измен€йте 
		/// содержимое этого метода с помощью редактора кода.
		/// </summary>
		void InitializeComponent(void)
		{
			System::ComponentModel::ComponentResourceManager^ resources = (gcnew System::ComponentModel::ComponentResourceManager(MyForm::typeid));
			this->pathToFile_box = (gcnew System::Windows::Forms::TextBox());
			this->enthropy_textbox = (gcnew System::Windows::Forms::TextBox());
			this->Remove_NoneRussian_without_spaces = (gcnew System::Windows::Forms::Button());
			this->Remove_NoneRussian_with_spaces = (gcnew System::Windows::Forms::Button());
			this->Result_box = (gcnew System::Windows::Forms::TextBox());
			this->CountLetter_button = (gcnew System::Windows::Forms::Button());
			this->bigramm_overlapped = (gcnew System::Windows::Forms::Button());
			this->bigramm_not_overlapped = (gcnew System::Windows::Forms::Button());
			this->label1 = (gcnew System::Windows::Forms::Label());
			this->SuspendLayout();
			// 
			// pathToFile_box
			// 
			this->pathToFile_box->BorderStyle = System::Windows::Forms::BorderStyle::FixedSingle;
			this->pathToFile_box->Location = System::Drawing::Point(12, 12);
			this->pathToFile_box->MaxLength = 8191;
			this->pathToFile_box->Name = L"pathToFile_box";
			this->pathToFile_box->Size = System::Drawing::Size(350, 20);
			this->pathToFile_box->TabIndex = 0;
			// 
			// enthropy_textbox
			// 
			this->enthropy_textbox->Location = System::Drawing::Point(12, 38);
			this->enthropy_textbox->MaxLength = 31;
			this->enthropy_textbox->Name = L"enthropy_textbox";
			this->enthropy_textbox->ReadOnly = true;
			this->enthropy_textbox->Size = System::Drawing::Size(350, 20);
			this->enthropy_textbox->TabIndex = 1;
			// 
			// Remove_NoneRussian_without_spaces
			// 
			this->Remove_NoneRussian_without_spaces->Location = System::Drawing::Point(13, 65);
			this->Remove_NoneRussian_without_spaces->Name = L"Remove_NoneRussian_without_spaces";
			this->Remove_NoneRussian_without_spaces->Size = System::Drawing::Size(82, 23);
			this->Remove_NoneRussian_without_spaces->TabIndex = 2;
			this->Remove_NoneRussian_without_spaces->Tag = L"with_spaces";
			this->Remove_NoneRussian_without_spaces->Text = L"Remove text";
			this->Remove_NoneRussian_without_spaces->UseVisualStyleBackColor = true;
			this->Remove_NoneRussian_without_spaces->Click += gcnew System::EventHandler(this, &MyForm::Remove_NoneRussian_Click);
			// 
			// Remove_NoneRussian_with_spaces
			// 
			this->Remove_NoneRussian_with_spaces->Location = System::Drawing::Point(101, 65);
			this->Remove_NoneRussian_with_spaces->Name = L"Remove_NoneRussian_with_spaces";
			this->Remove_NoneRussian_with_spaces->Size = System::Drawing::Size(94, 23);
			this->Remove_NoneRussian_with_spaces->TabIndex = 3;
			this->Remove_NoneRussian_with_spaces->Tag = L"without_spaces";
			this->Remove_NoneRussian_with_spaces->Text = L"Rmv w/ spaces";
			this->Remove_NoneRussian_with_spaces->UseVisualStyleBackColor = true;
			this->Remove_NoneRussian_with_spaces->Click += gcnew System::EventHandler(this, &MyForm::Remove_NoneRussian_Click);
			// 
			// Result_box
			// 
			this->Result_box->Location = System::Drawing::Point(369, 12);
			this->Result_box->MaxLength = 16383;
			this->Result_box->Multiline = true;
			this->Result_box->Name = L"Result_box";
			this->Result_box->ReadOnly = true;
			this->Result_box->ScrollBars = System::Windows::Forms::ScrollBars::Vertical;
			this->Result_box->Size = System::Drawing::Size(369, 216);
			this->Result_box->TabIndex = 4;
			// 
			// CountLetter_button
			// 
			this->CountLetter_button->Location = System::Drawing::Point(202, 64);
			this->CountLetter_button->Name = L"CountLetter_button";
			this->CountLetter_button->Size = System::Drawing::Size(160, 23);
			this->CountLetter_button->TabIndex = 5;
			this->CountLetter_button->Text = L"Count frequency (letters)";
			this->CountLetter_button->UseVisualStyleBackColor = true;
			this->CountLetter_button->Click += gcnew System::EventHandler(this, &MyForm::CountLetter_Click);
			// 
			// bigramm_overlapped
			// 
			this->bigramm_overlapped->Location = System::Drawing::Point(13, 94);
			this->bigramm_overlapped->Name = L"bigramm_overlapped";
			this->bigramm_overlapped->Size = System::Drawing::Size(182, 40);
			this->bigramm_overlapped->TabIndex = 6;
			this->bigramm_overlapped->Tag = L"overlapped";
			this->bigramm_overlapped->Text = L"Count frequency (bigramms overlapped)";
			this->bigramm_overlapped->UseVisualStyleBackColor = true;
			this->bigramm_overlapped->Click += gcnew System::EventHandler(this, &MyForm::CountBigramm_Click);
			// 
			// bigramm_not_overlapped
			// 
			this->bigramm_not_overlapped->Location = System::Drawing::Point(202, 94);
			this->bigramm_not_overlapped->Name = L"bigramm_not_overlapped";
			this->bigramm_not_overlapped->Size = System::Drawing::Size(160, 40);
			this->bigramm_not_overlapped->TabIndex = 7;
			this->bigramm_not_overlapped->Tag = L"not_overlapped";
			this->bigramm_not_overlapped->Text = L"Count frequency (bigramms NOT overlapped)";
			this->bigramm_not_overlapped->UseVisualStyleBackColor = true;
			this->bigramm_not_overlapped->Click += gcnew System::EventHandler(this, &MyForm::CountBigramm_Click);
			// 
			// label1
			// 
			this->label1->AutoSize = true;
			this->label1->ForeColor = System::Drawing::SystemColors::AppWorkspace;
			this->label1->Location = System::Drawing::Point(13, 214);
			this->label1->Name = L"label1";
			this->label1->Size = System::Drawing::Size(212, 13);
			this->label1->TabIndex = 8;
			this->label1->Text = L"FB-22 Punko Artem, FB-22 Rudenko Polina";
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(750, 240);
			this->Controls->Add(this->label1);
			this->Controls->Add(this->bigramm_not_overlapped);
			this->Controls->Add(this->bigramm_overlapped);
			this->Controls->Add(this->CountLetter_button);
			this->Controls->Add(this->Result_box);
			this->Controls->Add(this->Remove_NoneRussian_with_spaces);
			this->Controls->Add(this->Remove_NoneRussian_without_spaces);
			this->Controls->Add(this->enthropy_textbox);
			this->Controls->Add(this->pathToFile_box);
			this->FormBorderStyle = System::Windows::Forms::FormBorderStyle::FixedSingle;
			this->Icon = (cli::safe_cast<System::Drawing::Icon^>(resources->GetObject(L"$this.Icon")));
			this->MaximizeBox = false;
			this->Name = L"MyForm";
			this->Text = L"Crypto Lab 1";
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion

	private:
		void ShowPlaceholder();
		void HidePlaceholder();
		void pathToFile_box_GotFocus(Object^ sender, EventArgs^ e);
		void pathToFile_box_LostFocus(Object^ sender, EventArgs^ e);
		void pathToFile_DoubleClick(Object^ sender, EventArgs^ e);
		void Remove_NoneRussian_Click(System::Object^ sender, System::EventArgs^ e);
		void CountLetter_Click(System::Object^ sender, System::EventArgs^ e);
		void CountBigramm_Click(System::Object^ sender, System::EventArgs^ e);
};
}

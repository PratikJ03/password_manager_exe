# 🔐 Password Manager (Python + Tkinter)

A simple desktop **Password Manager application** built using **Python and Tkinter**.  
It allows users to generate, store, view, edit, and manage passwords using a master passcode.

---

## ✨ Features

- 🔑 Generate strong random passwords  
- 💾 Save credentials securely in a JSON file  
- 🔐 Master passcode protection  
- 👁️ View stored passwords in a separate window  
- ✏️ Edit existing credentials  
- 🗑️ Delete saved entries  
- 📋 Copy email or password to clipboard  
- 🪟 User-friendly Tkinter GUI  
- 🖥️ Packaged as a Windows executable using PyInstaller  

---

## 🛠️ Technologies Used

- Python  
- Tkinter  
- JSON  
- PyInstaller  

---

## 🔐 Master Passcode

The default master passcode to view and manage stored passwords is: 1234


> ⚠️ The passcode can be changed from inside the **View Passwords** window.

---

## ▶️ How to Run (Windows Executable)

1. Download the latest version from the **Releases** section.
2. Open the `dist` folder.
3. Run: main.exe


✅ No Python installation is required.

---

## 🐍 How to Run Using Python (Source Code)

Make sure Python is installed, then run:

```bash
python main.py


PasswordManager/
│
├── main.py
├── logo.png
├── data.json        (created automatically)
├── master.txt       (stores master passcode)
├── dist/
│   └── main.exe
└── README.md





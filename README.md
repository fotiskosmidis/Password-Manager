# Password Manager

A linux only password manager with a modern Tkinter GUI, secure AES-256 encryption, and C++ backend for performance.

## Features

- **Secure Storage:** All account data is encrypted using AES-256 and a key derived from your master password (hashed with SHA-256).
- **Modern GUI:** User-friendly interface built with Tkinter.
- **C++ Backend:** Core logic and encryption handled in C++ for speed, exposed to Python via pybind11.
- **Account Management:** Add, view, and manage multiple accounts.

## Project Structure

```
Password-Manager/
├── main.py                # Python entry point
├── frontEnd/              # Tkinter GUI components
│   ├── mainWindow.py
│   ├── loginWindow.py
│   ├── createPasswdWindow.py
│   └── addWindow.py
├── src/                   # C++ backend source code
│   ├── account.cpp
│   ├── account.h
│   ├── func.cpp
│   ├── func.h
│   ├── security.cpp
│   ├── security.h
│   └── bindings.cpp       # pybind11 bindings
├── CMakeLists.txt         # CMake build configuration
└── README.md
```

## Getting Started

### Libraries used

- [pybind11](https://github.com/pybind/pybind11)
- [nlohmann/json](https://github.com/nlohmann/json)
- [OpenSSL](https://www.openssl.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

## Usage

- On first launch, you’ll be prompted to create a master password (PIN).
- Use the GUI to add, view, and manage your accounts.
- All sensitive data is encrypted and stored in [.local/share/PasswordManager]
- You can reset the pin by deleting the json files. You must delete both files if you wanna reset. It will delete the accounts too.

## Security

- **Encryption:** AES-256-CBC with a key derived from your master password using SHA-256.
- **No plaintext storage:** All account fields are encrypted before being saved.

---
*Made with C++ and Python.*
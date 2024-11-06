# Password Manager

A simple command-line password manager that securely stores and retrieves encrypted passwords. This MVP (Minimum Viable Product) project demonstrates basic password management functionality using the Fernet symmetric encryption scheme.

## 🎯 Credits
This project was developed as part of the "4 days 4 projects" initiative by [Pythonando](https://pythonando.com.br) on YouTube.

## 🔑 Features
- Secure password encryption using Fernet (symmetric encryption)
- Save passwords for different domains
- Retrieve passwords using encryption key
- Local storage of encrypted passwords
- Key management system

## 🏗️ Project Structure
```
password-manager/
├── model/
│   └── password.py      # Base models and Password class
├── views/
│   └── password_views.py # Encryption/decryption logic
├── db/                  # Database directory for stored passwords
├── keys/               # Directory for key storage
└── templates.py        # CLI interface
```

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- cryptography package

### Installation
1. Clone the repository
```bash
git clone https://github.com/Caio-Felice-Cunha/Passwd-Manag.git
cd Passwd-Manag
```

2. Install required packages
```bash
pip install cryptography
```

### Usage
1. Run the application:
```bash
python templates.py
```

2. Choose an option:
   - Press 1 to save a new password
   - Press 2 to retrieve a password

3. For first-time use:
   - The system will generate an encryption key
   - Save this key securely - it's required to decrypt your passwords
   - The key will also be saved in the keys directory (remove after securing it elsewhere)

4. Follow the prompts to:
   - Enter the domain (e.g., "gmail.com")
   - Enter the password to encrypt
   - Provide your encryption key when retrieving passwords

## 🔒 Security Features
- Fernet symmetric encryption for password protection
- Secure random string generation for keys
- SHA-256 hashing implementation
- Base64 encoding for key storage

## ⚠️ Important Notes
- This is an MVP (Minimum Viable Product) designed for educational purposes
- Store your encryption key securely - lost keys mean lost passwords
- The system uses local file storage for passwords
- Remove key files from the keys directory after securing them elsewhere

## 🛠️ Technical Implementation
- `BaseModel`: Handles file-based storage operations
- `Password`: Manages password entries with domains
- `FernetHasher`: Implements encryption/decryption logic using Fernet
- Local storage using text files with "|" as delimiter

## 🚧 Limitations (MVP Version)
- Basic command-line interface
- Local file-based storage
- No user authentication system
- Single encryption key for all passwords
- No password strength validation
- No backup/restore functionality

## 🤝 Contributing
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License
This project is available as open source under the terms of the MIT License.

---
*Note: This is an MVP project created for educational purposes. For production use, consider additional security measures and features.*
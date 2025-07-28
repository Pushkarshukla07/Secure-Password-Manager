# 🔐 Secure Password Manager

A secure and efficient password manager built with Python. This tool allows you to safely store, retrieve, and generate strong passwords using encryption and a master password system.

---

## 📦 Features

- AES encryption using `cryptography`'s Fernet.
- Secure master password (hashed using `bcrypt`).
- Password storage in a hidden directory.
- Auto-copy passwords to clipboard with `pyperclip`.
- Strong password generator.
- CLI-based user interface.

---

## 🛠️ Requirements

Install dependencies via pip:

```bash
pip install cryptography bcrypt pyperclip
```

---

## ▶️ Usage

1. **Run the program**:
   ```bash
   python main.py
   ```

2. **On first run**, set up your master password.

3. Choose options:
   - Add a new password
   - Retrieve an existing password
   - Generate a strong password

---

## 📁 File Structure

```
SecurePasswordManager/
│
├── main.py           # Main application script
├── README.md         # Project documentation
```

> Note: Stored passwords and encryption key are saved in your home directory under `.password_manager`.

---

## 🔒 Security Notes

- Master password is hashed using `bcrypt`.
- Passwords are encrypted using Fernet (symmetric AES encryption).
- Nothing is stored in plain text.

---

## 👨‍💻 Author

Pushkar Shukla  
[GitHub](https://github.com/Pushkarshukla07) | [LinkedIn](https://linkedin.com/in/shuklapushkar)

---

## 📜 License

This project is licensed under the MIT License.

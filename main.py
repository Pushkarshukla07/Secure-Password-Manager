import os
import pickle
import pyperclip
import getpass
import bcrypt
from cryptography.fernet import Fernet
import secrets
import string

# ---------- Paths ----------
BASE_DIR = os.path.expanduser("~")
DATA_DIR = os.path.join(BASE_DIR, ".password_manager")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

PASS_FILE = os.path.join(DATA_DIR, "data.pkl")
MASTER_PASS_FILE = os.path.join(DATA_DIR, "master.hash")
FERNET_KEY_FILE = os.path.join(DATA_DIR, "key.key")

# ---------- Security ----------
def generate_key():
    key = Fernet.generate_key()
    with open(FERNET_KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(FERNET_KEY_FILE):
        return generate_key()
    with open(FERNET_KEY_FILE, 'rb') as f:
        return f.read()

fernet = Fernet(load_key())

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

# ---------- Data Management ----------
def load_data():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_data(data):
    with open(PASS_FILE, 'wb') as f:
        pickle.dump(data, f)

# ---------- Master Password ----------
def setup_master_password():
    if os.path.exists(MASTER_PASS_FILE):
        return

    print("\n🔐 Set up your master password:")
    password = getpass.getpass("Enter master password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password == confirm:
        hashed = hash_password(password)
        with open(MASTER_PASS_FILE, 'wb') as f:
            f.write(hashed)
        print("✅ Master password set successfully.\n")
    else:
        print("❌ Passwords do not match. Try again.")
        setup_master_password()

def authenticate():
    if not os.path.exists(MASTER_PASS_FILE):
        setup_master_password()

    with open(MASTER_PASS_FILE, 'rb') as f:
        stored_hash = f.read()

    for _ in range(3):
        password = getpass.getpass("🔑 Enter master password: ")
        if check_password(password, stored_hash):
            print("✅ Access Granted\n")
            return True
        else:
            print("❌ Incorrect password.")
    return False

# ---------- Features ----------
def add_password():
    data = load_data()
    account = input("🔖 Enter account name: ")
    password = getpass.getpass("🔐 Enter password: ")
    encrypted_pass = fernet.encrypt(password.encode())
    data[account] = encrypted_pass
    save_data(data)
    print(f"✅ Password for '{account}' saved successfully.\n")

def get_password():
    data = load_data()
    account = input("🔎 Enter account name to retrieve password: ")
    if account in data:
        decrypted_pass = fernet.decrypt(data[account]).decode()
        pyperclip.copy(decrypted_pass)
        print(f"📋 Password copied to clipboard: {decrypted_pass}\n")
    else:
        print("❌ Account not found.\n")

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    print(f"🔐 Generated Password: {password}")
    pyperclip.copy(password)
    print("📋 Password copied to clipboard.\n")

# ---------- Main Program ----------
def menu():
    while True:
        print("==== Password Manager ====")
        print("1️⃣ Add new password")
        print("2️⃣ Retrieve password")
        print("3️⃣ Generate strong password")
        print("4️⃣ Exit")
        choice = input("➡️ Enter your choice: ")

        if choice == '1':
            add_password()
        elif choice == '2':
            get_password()
        elif choice == '3':
            generate_password()
        elif choice == '4':
            print("👋 Exiting... Stay secure!")
            break
        else:
            print("❌ Invalid choice, try again.\n")

if __name__ == "__main__":
    if authenticate():
        menu()

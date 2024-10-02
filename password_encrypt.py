import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the password
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# GUI Functions
def encrypt():
    password = password_entry.get()
    if password:
        encrypted = encrypt_password(password)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, encrypted)
    else:
        messagebox.showwarning("Warning", "Please enter a password to encrypt.")

def decrypt():
    encrypted_password = output_entry.get()
    if encrypted_password:
        try:
            decrypted = decrypt_password(encrypted_password.encode())
            output_entry.delete(0, tk.END)
            output_entry.insert(0, decrypted)
        except Exception:
            messagebox.showerror("Error", "Invalid encrypted password.")
    else:
        messagebox.showwarning("Warning", "Please enter an encrypted password to decrypt.")

# Set up the main window
root = tk.Tk()
root.title("Password Encryption App")

# Generate the key if it doesn't exist
try:
    load_key()
except FileNotFoundError:
    generate_key()

# Create input fields and buttons
password_label = tk.Label(root, text="Enter Password:")
password_label.pack(pady=5)

password_entry = tk.Entry(root, width=50, show='*')
password_entry.pack(pady=5)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt)
decrypt_button.pack(pady=5)

output_label = tk.Label(root, text="Output (Encrypted/Decrypted):")
output_label.pack(pady=5)

output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)

# Start the GUI loop
root.mainloop()
import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet
import json
import os




# Load or generate key
def load_key():
    if os.path.exists("secret.key"):
        return open("secret.key", "rb").read()
    else:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

# Encrypt and decrypt functions
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# Save passwords to a JSON file
def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

# Load passwords from a JSON file
def load_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as f:
            return json.load(f)
    return {}

# Master password check
def check_master_password():
    master_password = simpledialog.askstring("Master Password", "Enter master password:", show='*')
    if master_password == 'test':  # Replace 'your_master_password' with the actual master password
        return True
    else:
        messagebox.showerror("Error", "Incorrect master password!")
        root.destroy()  # Close the application if the password is incorrect
        return False

# GUI Functions
def add_password():
    website = simpledialog.askstring("Input", "Enter website:")
    password = simpledialog.askstring("Input", "Enter password:")
    
    if website and password:
        encrypted_password = encrypt_password(password)
        passwords[website] = encrypted_password
        save_passwords(passwords)
        refresh_password_list()
    else:
        messagebox.showwarning("Warning", "Please enter both website and password.")

def retrieve_password():
    website = simpledialog.askstring("Input", "Enter website to retrieve password:")
    if website in passwords:
        decrypted_password = decrypt_password(passwords[website])
        messagebox.showinfo("Password", f"Password for {website}: {decrypted_password}")
    else:
        messagebox.showerror("Error", "Website not found.")

def refresh_password_list():
    password_list.delete(0, tk.END)
    for website in passwords.keys():
        password_list.insert(tk.END, website)

# Set up the main window
root = tk.Tk()
root.title("Password Manager")

# Load existing passwords
passwords = load_passwords()

# Master password check before anything else
if not check_master_password():
    root.quit()  # Exit if the master password check fails

# Create buttons and list box
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.pack(pady=5)

retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_password)
retrieve_button.pack(pady=5)

password_list = tk.Listbox(root, width=50)
password_list.pack(pady=10)

# Refresh the list on startup
refresh_password_list()

# Start the GUI loop
root.mainloop()
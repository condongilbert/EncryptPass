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

if __name__ == "__main__":
    # Generate a key only once and save it
    generate_key()

    # Example usage
    password = input("Enter the password to encrypt: ")
    encrypted = encrypt_password(password)
    print(f"Encrypted password: {encrypted}")

    decrypted = decrypt_password(encrypted)
    print(f"Decrypted password: {decrypted}")
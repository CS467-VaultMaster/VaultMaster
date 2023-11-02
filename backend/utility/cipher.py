from Crypto.Cipher import AES
from hashlib import sha256
from binascii import hexlify, unhexlify
from cryptography.fernet import Fernet

salt = "SECRETSALT"

def derive_key(password, salt):
    return sha256(password.encode() + salt.encode()).digest()


def encrypt(data, password, salt):
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return hexlify(nonce + ciphertext).decode()


def decrypt(encrypted_data, password, salt):
    key = derive_key(password, salt)
    encrypted_data = unhexlify(encrypted_data.encode())
    nonce, ciphertext = encrypted_data[:16], encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()


# Generate fernet key
fernet_key = Fernet.generate_key()
data = "Hello, World! =+%%^$&*#@"
password = "85432b2a-7928-11ee-b962-0242ac120002"
salt = "SECRETSALT"

# ENCRYPTION
# Encode the fernet key
encrypted_f_key = encrypt(fernet_key.decode("ASCII"), password, salt)
# Save it to the credential row.
# Encrypt password with the original fernet_key
fernet1 = Fernet(fernet_key)
encrypted_data = fernet1.encrypt(data.encode())
# Save encrypted_data as the credential's password
print(encrypted_data.decode("ASCII"))

# DECRYPTION
# Decode the fernet key and encode it to byte string.
decrypted_f_key = decrypt(encrypted_f_key, password, salt).encode()
fernet2 = Fernet(decrypted_f_key)
decrypted_data = fernet2.decrypt(encrypted_data.decode())
print(decrypted_data.decode("ASCII"))

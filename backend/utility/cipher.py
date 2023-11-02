from Crypto.Cipher import AES
from hashlib import sha256
from binascii import hexlify, unhexlify

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
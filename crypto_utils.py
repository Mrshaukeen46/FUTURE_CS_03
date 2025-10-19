from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os
from pathlib import Path

# CONFIG
KEYFILE = Path('.key')  # store the raw AES key here locally (do NOT commit to git)
KEY_SIZE = 32  # AES-256
SALT_SIZE = 16
PBKDF2_ITER = 200000

def load_key():
    """
    Load AES key from KEYFILE. This file should be created securely using generate_key.py locally.
    For demo only: If not present, raise an error to avoid embedding secrets in the repo.
    """
    if not KEYFILE.exists():
        raise FileNotFoundError("Key file '.key' not found. Run `python generate_key.py` to create one locally.")
    return KEYFILE.read_bytes()

def pad(data):
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt_file(in_path, out_path):
    key = load_key()
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(in_path, 'rb') as f_in:
        plaintext = f_in.read()
    ciphertext = cipher.encrypt(pad(plaintext))
    # write iv + ciphertext
    with open(out_path, 'wb') as f_out:
        f_out.write(iv + ciphertext)

def decrypt_file(enc_path, out_path):
    key = load_key()
    with open(enc_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))
    with open(out_path, 'wb') as f_out:
        f_out.write(plaintext)

def list_encrypted_files(folder):
    p = Path(folder)
    if not p.exists():
        return []
    return sorted([f.name for f in p.iterdir() if f.is_file() and f.name.endswith('.enc')])

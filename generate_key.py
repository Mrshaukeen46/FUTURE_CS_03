from Crypto.Random import get_random_bytes
from pathlib import Path
KEYFILE = Path('.key')
if KEYFILE.exists():
    print(".key already exists. Delete or backup before generating a new one.")
else:
    key = get_random_bytes(32)  # AES-256
    KEYFILE.write_bytes(key)
    # set restrictive permissions (POSIX), best effort on Windows
    try:
        KEYFILE.chmod(0o600)
    except Exception:
        pass
    print("Generated .key file (32 bytes). Keep this secret and DO NOT commit to GitHub.")
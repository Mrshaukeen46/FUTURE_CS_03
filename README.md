# Secure File Sharing System (Task 3) — Future Interns

**Demo project** implementing a simple secure file-sharing system using **Flask** and **AES-256 encryption**.
This repo is intended for educational/demo purposes and is structured so you can upload it directly to GitHub.

## Features
- Upload files via web UI
- Files are encrypted with AES-256 (CBC) before being saved to disk
- Download endpoint decrypts files on-the-fly and sends them to the client
- Simple key-management helper script to create a local `.key` file
- Clear instructions & security considerations in `SECURITY_OVERVIEW.md`

## Quickstart (local, safe demo)
1. Clone repo and create a Python virtualenv.
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Generate a local key (do not commit this file):
```bash
python generate_key.py
```
4. Run the Flask app:
```bash
python app.py
```
5. Visit `http://127.0.0.1:5000` to upload/download files.

## Important Notes
- **Do NOT commit `.key` to GitHub.** It's ignored by `.gitignore`.
- This demo uses a local key file for simplicity. For production, use an HSM or cloud KMS (AWS KMS, Azure Key Vault).
- Validate and harden file type checks, storage permissions, TLS, authentication, and rate limiting before any real-world use.

## Files in this repo
- `app.py` — Flask app
- `crypto_utils.py` — AES encrypt/decrypt helpers (PyCryptodome)
- `generate_key.py` — helper to create `.key` file locally
- `templates/index.html` — simple upload/list UI
- `requirements.txt`
- `SECURITY_OVERVIEW.md` — detailed security report & guidance
- `.gitignore` — ignores keys and uploads

---
*Generated on 2025-10-19*

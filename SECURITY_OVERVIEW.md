# SECURITY OVERVIEW — Secure File Sharing System (Task 3)

## Project Summary
This project demonstrates building a simple secure file sharing system with a focus on encrypting files at rest and in transit. The demo uses **AES-256 (CBC mode)** via **PyCryptodome** to encrypt files before storage. Files are decrypted on download for the recipient.

**Important:** This is a learning/demo project. Follow the recommendations below before using any of this code in production.

## Architecture
- **Flask** web server provides upload, list, and download endpoints.
- Uploaded files are temporarily saved and then encrypted to `encrypted_files/<originalname>.enc`.
- Encryption uses a locally stored raw key (`.key`) — this is for demo only.
- Decryption occurs server-side when a user requests download; decrypted file created in `tmp/` and served to client.

## Cryptography Details
- **Algorithm:** AES-256 (CBC mode)
- **Key Size:** 256 bits (32 bytes)
- **IV:** Random 16-byte IV is prepended to the ciphertext file.
- **Padding:** PKCS#7 style padding implemented in `crypto_utils.py`.
- **Key Storage:** Key stored in `.key` file (binary, 32 bytes). **Do not commit** to version control.

## Threat Model & Risks
- **Threats mitigated:** Accidental exposure of files at rest, casual access to filesystem.
- **Remaining risks / not addressed by demo:**
  - Authentication and authorization (no user accounts in demo) — a major requirement for production.
  - Key compromise if `.key` is leaked or stored insecurely.
  - In-memory plaintext exposure during decryption before sending to client.
  - Lack of TLS termination guidance (Flask dev server is not TLS-enabled).

## Recommendations for Production Hardening
1. **Key Management:** Use a dedicated KMS or HSM (AWS KMS, Azure Key Vault, HashiCorp Vault). Do not store raw keys on disk.
2. **Authentication & Authorization:** Implement user accounts, file ACLs, RBAC, and fine-grained access control.
3. **Transport Security:** Run behind TLS (HTTPS) with correct certificates (Let’s Encrypt or enterprise CA).
4. **Ephemeral Decryption:** Stream decrypt to response and avoid writing plaintext to disk when possible.
5. **Logging & Auditing:** Log access events, maintain audit trails, and monitor for suspicious downloads.
6. **Rate Limiting & Validation:** Prevent abuse by adding rate-limiting, file size limits, virus scanning, and strict MIME/type checks.
7. **Secure Defaults:** Restrict file permissions, run app with least privilege, and perform regular dependency updates.
8. **CI/CD Security Gates:** Integrate static analysis, SCA (software composition analysis), and automated security testing in the pipeline.

## How to Test (Suggested)
- Generate a key with `python generate_key.py`.
- Start app and upload a small text file. Confirm encrypted file exists in `encrypted_files/` with `.enc` suffix.
- Download and verify the file contents match the original.
- Inspect encrypted file: first 16 bytes are IV, remainder is ciphertext.

## Files for Submission
- `app.py`, `crypto_utils.py`, `generate_key.py`, `templates/`, `requirements.txt`
- `SECURITY_OVERVIEW.md` (this file) — include in repository root.
- `README.md` — project instructions and usage.

---
*Security overview generated 2025-10-19*

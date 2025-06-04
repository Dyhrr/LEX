import os
import json
import base64
import getpass
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

PASS_FILE = os.path.join("memory", "passphrase.json")


def _read_file() -> tuple[bytes, bytes] | None:
    """Return salt and hash from disk if present."""
    if not os.path.exists(PASS_FILE):
        return None
    try:
        with open(PASS_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        salt = base64.b64decode(data.get("salt", ""))
        stored_hash = bytes.fromhex(data.get("hash", ""))
        if salt and stored_hash:
            return salt, stored_hash
    except Exception:
        pass
    return None


def _write_file(salt: bytes, hash_bytes: bytes) -> None:
    os.makedirs(os.path.dirname(PASS_FILE), exist_ok=True)
    with open(PASS_FILE, "w", encoding="utf-8") as fh:
        json.dump(
            {"salt": base64.b64encode(salt).decode(), "hash": hash_bytes.hex()}, fh
        )


def _hash_passphrase(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 200000)


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))


def require_vault_key() -> bytes:
    """Prompt for a passphrase and return a Fernet key."""
    data = _read_file()
    if not data:
        # First run: set new passphrase
        while True:
            pwd = getpass.getpass("[Lex] Set passphrase: ")
            confirm = getpass.getpass("[Lex] Confirm passphrase: ")
            if pwd and pwd == confirm:
                salt = os.urandom(16)
                h = _hash_passphrase(pwd, salt)
                _write_file(salt, h)
                return _derive_key(pwd, salt)
            print("[Lex] Passphrases did not match. Try again.")
    else:
        salt, stored = data
        for _ in range(3):
            pwd = getpass.getpass("[Lex] Enter passphrase: ")
            if _hash_passphrase(pwd, salt) == stored:
                return _derive_key(pwd, salt)
            print("[Lex] Incorrect passphrase.")
        raise SystemExit("[Lex] Too many incorrect passphrase attempts.")

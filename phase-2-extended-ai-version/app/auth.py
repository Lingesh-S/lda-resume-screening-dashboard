"""Local JSON user store with salted, hashed passwords.

This is a demo-grade store for a single-machine Streamlit app. Passwords are
never written in plain text: each one is hashed with PBKDF2-HMAC-SHA256 and a
random per-user salt. For anything multi-user or internet-facing, use a real
identity provider instead.
"""

import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path

PBKDF2_ITERATIONS = 600_000
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "ai_components" / "users.json"


def get_db_path() -> Path:
    """Location of the user store; override with the USER_DB_PATH env var."""
    return Path(os.environ.get("USER_DB_PATH", DEFAULT_DB_PATH))


def hash_password(password: str, salt: bytes | None = None) -> str:
    """Return `pbkdf2_sha256$<iterations>$<salt hex>$<hash hex>`."""
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Constant-time check of `password` against a value from `hash_password`."""
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$")
    except (AttributeError, ValueError):
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
    )
    return hmac.compare_digest(digest.hex(), digest_hex)


def load_db(path: Path | None = None) -> dict:
    path = Path(path or get_db_path())
    if not path.exists() or path.stat().st_size == 0:
        return {"users": []}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save_db(data: dict, path: Path | None = None) -> None:
    path = Path(path or get_db_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=4)
    tmp.replace(path)


def initialize_database(path: Path | None = None) -> None:
    path = Path(path or get_db_path())
    if not path.exists():
        save_db({"users": []}, path)


def find_user(email: str, path: Path | None = None) -> dict | None:
    email = email.strip().lower()
    return next((u for u in load_db(path)["users"] if u["email"].lower() == email), None)


def create_user(name: str, email: str, age: int, sex: str, password: str, path: Path | None = None) -> dict:
    """Add a user; raises ValueError for a missing field or a duplicate email."""
    email = email.strip().lower()
    if not name.strip() or not email or not password:
        raise ValueError("Name, email and password are required.")
    data = load_db(path)
    if any(u["email"].lower() == email for u in data["users"]):
        raise ValueError("An account with this email already exists.")
    user = {
        "name": name.strip(),
        "email": email,
        "age": age,
        "sex": sex,
        "password_hash": hash_password(password),
        "resume": None,
        "job_description": None,
        "job_applied": None,
        "score": "0",
        "questions": None,
    }
    data["users"].append(user)
    save_db(data, path)
    return user


def authenticate(email: str, password: str, path: Path | None = None) -> dict | None:
    """Return the user if the credentials match, else None."""
    user = find_user(email, path)
    if user and verify_password(password, user.get("password_hash", "")):
        return user
    return None


def update_user(email: str, updates: dict, path: Path | None = None) -> dict | None:
    """Merge `updates` into the stored user and return it (None if not found)."""
    data = load_db(path)
    for user in data["users"]:
        if user["email"].lower() == email.strip().lower():
            user.update(updates)
            save_db(data, path)
            return user
    return None

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_security():
    password = "test12345"

    hashed = hash_password(password)
    print("Hashed password:", hashed)

    is_valid = verify_password(password, hashed)
    print("Password valid:", is_valid)

    token = create_access_token(
        {
            "sub": "test@example.com",
            "user_id": 1,
        }
    )

    print("Access token:", token)

    payload = decode_access_token(token)
    print("Decoded payload:", payload)


if __name__ == "__main__":
    test_security()
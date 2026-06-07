from app.core.database import get_db_connection
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def get_user_by_email(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email, username, hashed_password, created_at
        FROM users
        WHERE email = ?;
        """,
        (email,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


def get_user_by_id(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email, username, created_at
        FROM users
        WHERE id = ?;
        """,
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)


def create_user(email: str, username: str, password: str):
    existing_user = get_user_by_email(email)

    if existing_user:
        raise ValueError("A user with this email already exists.")

    hashed_password = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (email, username, hashed_password)
        VALUES (?, ?, ?);
        """,
        (email, username, hashed_password),
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return get_user_by_id(user_id)


def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)

    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    safe_user = {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "created_at": user["created_at"],
    }

    return safe_user


def create_auth_response(user: dict):
    token = create_access_token(
        {
            "sub": user["email"],
            "user_id": user["id"],
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user,
    }
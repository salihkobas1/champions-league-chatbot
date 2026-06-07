import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from app.services.chat_history_service import (
    get_or_create_default_chat_session,
    save_chat_message,
    get_default_chat_messages_for_user,
    clear_default_chat_for_user,
)


def test_chat_history():
    user_id = 1

    session = get_or_create_default_chat_session(user_id)
    print("Session:", session)

    save_chat_message(
        chat_id=session["id"],
        user_id=user_id,
        role="user",
        content="Who is the 5th highest goalscorer?",
        route=None,
    )

    save_chat_message(
        chat_id=session["id"],
        user_id=user_id,
        role="bot",
        content="The requested ranked goalscorer is Raúl González, with 71 goals for Spain.",
        route="sql",
    )

    data = get_default_chat_messages_for_user(user_id)
    print("Messages:")
    for message in data["messages"]:
        print(message)

    clear_result = clear_default_chat_for_user(user_id)
    print("Clear result:", clear_result)


if __name__ == "__main__":
    test_chat_history()
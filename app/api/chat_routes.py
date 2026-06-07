from fastapi import APIRouter, Depends

from app.schemas.chat_schema import ChatRequest
from app.services.chat_service import answer_question
from app.core.auth_dependency import get_current_user
from app.services.chat_history_service import (
    get_or_create_default_chat_session,
    save_chat_message,
    get_default_chat_messages_for_user,
    clear_default_chat_for_user,
)


router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    chat_session = get_or_create_default_chat_session(user_id)

    save_chat_message(
        chat_id=chat_session["id"],
        user_id=user_id,
        role="user",
        content=request.message,
        route=None,
    )

    result = answer_question(request.message)

    save_chat_message(
        chat_id=chat_session["id"],
        user_id=user_id,
        role="bot",
        content=result["answer"],
        route=result["route"],
    )

    result["user"] = {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"],
    }

    result["chat_session"] = chat_session

    return result


@router.get("/chat/history")
def get_chat_history(
    current_user: dict = Depends(get_current_user),
):
    data = get_default_chat_messages_for_user(current_user["id"])

    return data


@router.delete("/chat/history")
def clear_chat_history(
    current_user: dict = Depends(get_current_user),
):
    result = clear_default_chat_for_user(current_user["id"])

    return result
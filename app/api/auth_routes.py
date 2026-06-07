from fastapi import APIRouter, HTTPException, Depends

from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
)
from app.services.auth_service import (
    create_user,
    authenticate_user,
    create_auth_response,
)
from app.core.auth_dependency import get_current_user


router = APIRouter()


@router.post("/auth/register", response_model=AuthResponse)
def register(request: RegisterRequest):
    try:
        user = create_user(
            email=request.email,
            username=request.username,
            password=request.password,
        )

        return create_auth_response(user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/auth/login", response_model=AuthResponse)
def login(request: LoginRequest):
    user = authenticate_user(
        email=request.email,
        password=request.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    return create_auth_response(user)


@router.get("/auth/me")
def me(current_user: dict = Depends(get_current_user)):
    return {
        "user": current_user
    }
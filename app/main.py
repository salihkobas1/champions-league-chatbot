from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat_routes import router as chat_router

from app.api.health_routes import router as health_router
app = FastAPI(
    title="Champions League Chatbot Backend",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development için böyle kalsın, sonra frontend URL ile sınırlarız
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(health_router, prefix="/api", tags=["health"])

@app.get("/")
def root():
    return {
        "message": "Champions League Chatbot Backend is running."
    }
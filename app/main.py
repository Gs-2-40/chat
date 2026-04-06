from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.websocket import router as ws_router
from app.api.messages import router as static_router

app = FastAPI()

# "Монтируем" роутер в приложение
app.include_router(auth_router)
app.include_router(ws_router)
app.include_router(static_router)
from fastapi import FastAPI
from api.auth import router as auth_router
from websocket import router as ws_router
from api.messages import router as static_router

app = FastAPI()

# "Монтируем" роутер в приложение
app.include_router(auth_router)
app.include_router(ws_router)
app.include_router(static_router)
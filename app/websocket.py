from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Cookie, Depends, status
from services.connection import ConnectionManager
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from core.config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/ws", tags=["WebSocket"])

manager = ConnectionManager()

async def get(data, user_id, db):
    pass

async def send(data, user_id, db):
    pass

actions = {
    "get": get,
    "send": send
}

@router.websocket("/")
async def websockets_endpoint(websocket: WebSocket,
    # Браузер отправит куки автоматически, FastAPI их поймает
    access_token: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db)
    ):
    await websocket.accept()
    
    # Ручная проверка внутри сокета
    if not access_token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:

        await manager.connect(str(user_id), websocket)
        while True:
            try:
                # 1. Получаем JSON
                data = await websocket.receive_json()
                action = data.get("action")

                # 2. Ищем нужный обработчик
                handler = actions.get(action)
                
                if handler:
                    # 3. Запускаем логику
                    await handler(data, user_id, db)
                else:
                    await websocket.send_json({"error": "Unknown action"})
                    
            except WebSocketDisconnect:
                manager.disconnect(user_id)
                break

    except WebSocketDisconnect:
        print('exception, closed')
        await manager.disconnect(str(user_id))

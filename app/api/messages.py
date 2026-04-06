from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.core.config import html

# Создаем объект роутера
# prefix — добавится ко всем путям в этом файле
# tags — поможет сгруппировать методы в документации Swagger (/docs)
router = APIRouter(prefix="/", tags=["static"])


@router.get("/ping")
async def root():
    return {"message": "pong"}

@router.get("/")
async def get():
    return HTMLResponse(html)

''' ARGS
(
    user_id: int = Depends(get_current_user), # Магия здесь
    db: AsyncSession = Depends(get_db)
)
'''
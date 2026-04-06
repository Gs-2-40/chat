from fastapi import APIRouter, requests, Depends, Response
from app.database import get_db
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import path_to_avatar

# Создаем объект роутера
# prefix — добавится ко всем путям в этом файле
# tags — поможет сгруппировать методы в документации Swagger (/docs)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(response: Response, db: AsyncSession = Depends(get_db)):
    '''Authorization function. Username, password.'''
    data = requests.json()
    if not data.get("username") or not data.get("password"):
        return {"message": "Login failed"}
    user = await db.query(User).filter(User.username == data.get("username")).first()
    if not user or not verify_password(data.get("password"), user.hashed_password):
        return {"message": "Login failed"}
    try:
        response.set_cookie(
        key="access_token", 
        value=create_access_token(user.id), 
        httponly=True,  # КРИТИЧНО: JS не сможет прочитать куку
        samesite="lax",
        secure=True     # Только для HTTPS
        )
    except Exception:
        return {"message": "Login failed"}
    return {"message": "Login success"}

@router.post("/registration")
async def registration(response: Response, db: AsyncSession = Depends(get_db)):
    '''Registration function. Username, password'''
    data = requests.json()
    if not data.get("username") or not data.get("password"):
        return {"message": "Registration failed"}
    user = await db.query(User).filter(User.username == data.get("username")).first()
    if user or len(data.get("password")) < 4:
        return {"message": "Registration failed"}
    try:
        db_user = User(username=data.get("username"), hashed_password=get_password_hash(data.get("password")), path_to_avatar=path_to_avatar)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return {"message": "Registration success"}
    except Exception:
        return {"message": "Login success"}

@router.get("/me")
async def get_me():
    return {"user": "current_user"}
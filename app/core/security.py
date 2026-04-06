import bcrypt
import jwt
import datetime
from fastapi import HTTPException, status, Cookie
from app.core.config import SECRET_KEY, ALGORITHM

async def get_current_user(
    # FastAPI сам посмотрит в куки и найдет там поле 'access_token'
    access_token: str | None = Cookie(default=None) 
) -> int:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы (кука пуста)"
        )
    
    try:
        # Декодируем токен
        payload = jwt.decode(
            access_token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        return int(user_id)
    except Exception:
        raise HTTPException(status_code=401, detail="Ошибка токена")

def create_access_token(user_id) -> str:
    payload = {
        "user_id": user_id,
        # 'exp' is a standard claim for expiration time
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.timezone.utc) # Issued at
    }
    
    # Encode the token using the HS256 algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # TODO: change key
    return token

def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
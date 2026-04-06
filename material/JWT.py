from fastapi import FastAPI, Cookie, Response

@app.post("/api/login")
async def login(response: Response):
    token = "eyJhbGci..." # Генерируем JWT
    # Устанавливаем куку
    response.set_cookie(
        key="access_token", 
        value=token, 
        httponly=True,  # КРИТИЧНО: JS не сможет прочитать куку
        samesite="lax",
        secure=True     # Только для HTTPS
    )
    return {"status": "ok"}

@app.get("/api/messages")
async def get_messages(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401)
    # Проверка jwt.decode(access_token, ...)
    return {"chats": "Твои секретные сообщения"}
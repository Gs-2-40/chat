from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class User(Base):
    '''Таблица пользователей - id username hashed_password path_to_avatar'''
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    path_to_avatar: Mapped[str] = mapped_column(String(100))
    def __repr__(self):
        return f"<User id={self.id} username={self.username} hashed_password={self.hashed_password} path_to_avatar={self.path_to_avatar}>"
 
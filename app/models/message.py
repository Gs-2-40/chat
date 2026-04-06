from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.user import User

class Message(Base):
    '''Таблица сообщений - id content sender receiver timestamp'''
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(100))
    sender: Mapped[User] = relationship(back_populates="messages")
    receiver: Mapped[User] = relationship(back_populates="messages")
    timestamp: Mapped[str] = mapped_column(String(100))
    def __repr__(self):
        return f"<Message id={self.id} content={self.content} sender={self.sender} receiver={self.receiver} timestamp={self.timestamp}>"

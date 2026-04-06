'''Database manager for massanger dinochat'''
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import User, Message, Base # models of db tables

DATABASE_URL = "sqlite+aiosqlite:///./dinochat.db"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # Нужно только для SQLite
)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class DataBaseManager:
    async def get_db():
        async with AsyncSessionLocal() as session:
            yield session
    
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    async def add_user(db, username, hashed_password, path_to_avatar):
        db_user = User(username=username, hashed_password=hashed_password, path_to_avatar=path_to_avatar)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def add_message(db, content, sender_id, receiver_id):
        db_message = Message(content=content, sender_id=sender_id, receiver_id=receiver_id)
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        return db_message

    async def get_user(db, username):
        return await db.query(User).filter(User.username == username).first()

    async def get_user_by_id(db, user_id):
        return await db.query(User).filter(User.id == user_id).first()
    
    async def get_all_users(db):
        return await db.query(User).all()
    
    async def get_all_messages(db):
        return await db.query(Message).all()
    
    async def get_messages_by_user(db, user_id):
        return await db.query(Message).filter(Message.sender_id == user_id).all()
    
    async def get_messages_by_sender_and_receiver(db, sender_id, receiver_id):
        return await db.query(Message).filter(Message.sender_id == sender_id, Message.receiver_id == receiver_id).all()
    
    async def get_messages_by_members(self, first_id, second_id):
        return await self.db_manager.get_messages_by_sender_and_receiver(first_id, second_id) + self.db_manager.get_messages_by_sender_and_receiver(second_id, first_id)
    
    async def get_messages_by_sender(db, sender_id):
        return await db.query(Message).filter(Message.sender_id == sender_id).all()
    
    async def get_messages_by_receiver(db, receiver_id):
        return await db.query(Message).filter(Message.receiver_id == receiver_id).all()
    
    async def get_message_by_id(db, message_id):
        return await db.query(Message).filter(Message.id == message_id).first()
    
    async def delete_message(db, message_id):
        message = await db.query(Message).filter(Message.id == message_id).first()
        db.delete(message)
        await db.commit()
        return message
    
    async def delete_user(db, user_id):
        user = await db.query(User).filter(User.id == user_id).first()
        db.delete(user)
        await db.commit()
        return user
    
    async def update_user(db, user_id, username=None, hashed_password=None, path_to_avatar=None):
        user = await db.query(User).filter(User.id == user_id).first()
        if username:
            user.username = username
        if hashed_password:
            user.hashed_password = hashed_password
        if path_to_avatar:
            user.path_to_avatar = path_to_avatar
        await db.commit()
        await db.refresh(user)
        return user
    
    async def update_message(db, message_id, content):
        message = await db.query(Message).filter(Message.id == message_id).first()
        message.content = content
        await db.commit()
        await db.refresh(message)
        return message
    
    async def delete_all_messages(db):
        messages = await db.query(Message).all()
        for message in messages:
            db.delete(message)
        await db.commit()
        return messages
    
    async def delete_all_users(db):
        users = await db.query(User).all()
        for user in users:
            db.delete(user)
        await db.commit()
        return users

    async def delete_all(db):
        await db.query(Message).delete()
        await db.query(User).delete()
        await db.commit()
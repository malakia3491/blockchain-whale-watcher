from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.persistance.models import User

class UserRepository:
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory
        self._cached_ids: set[int] = set()
        self._initialized = False

    async def _ensure_loaded(self):
        if not self._initialized:
            async with self._session_factory() as session:
                result = await session.execute(select(User.chat_id))
                self._cached_ids = set(result.scalars().all())
                self._initialized = True

    async def add_user(self, chat_id: int):
        await self._ensure_loaded()
        
        if chat_id in self._cached_ids:
            return 

        self._cached_ids.add(chat_id)

        async with self._session_factory() as session:
            user = User(chat_id=chat_id)
            session.add(user)
            await session.commit()
            
    async def get_all_ids(self) -> list[int]:
        await self._ensure_loaded()
        return list(self._cached_ids)
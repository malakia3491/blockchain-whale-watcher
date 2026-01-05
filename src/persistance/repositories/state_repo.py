from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.persistance.models import AppState

class StateRepository:
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory
        self._last_block: int | None = None
        self._record_id: UUID | None = None
        
    async def load_state(self):
        async with self._session_factory() as session:
            stmt = select(AppState).limit(1)
            result = await session.execute(stmt)
            state = result.scalars().first()
            
            if state:
                self._last_block = state.last_block
            else:
                self._last_block = None
            print(f"🔄 State loaded: {self._last_block}")

    def get_last_block(self) -> int | None:
        return self._last_block

    async def set_last_block(self, block_number: int):
        self._last_block = block_number
        
        async with self._session_factory() as session:
            stmt = select(AppState).limit(1)
            result = await session.execute(stmt)
            state_record = result.scalars().first()

            if state_record:
                state_record.last_block = block_number
            else:
                new_record = AppState(last_block=block_number)
                session.add(new_record)

            await session.commit()
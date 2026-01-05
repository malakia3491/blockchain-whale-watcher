import os
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ArgumentError

from src.domain import Config
from .models import BaseModel
from .repositories import UserRepository, StateRepository, TransactionRepository

class DbInitializator:
    def __init__(self, config: Config):
        self._config = config  
        self._is_initialized = False
    
    async def __create_session_fabric(self):
        try:
            engine = create_async_engine(self._config.db_connection, echo=False)
        except ArgumentError as ae:
            raise RuntimeError(f"Невалидная строка подключения к БД: {self._config.db_connection}") from ae
        except Exception as e:
            raise

        AsyncSessionLocalFabric = sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False
        )

        self._is_initialized = True
        return AsyncSessionLocalFabric
    
    async def initialize(self) -> tuple[UserRepository, StateRepository, TransactionRepository]:
        session_factory = await self.__create_session_fabric()
        
        state_repo = StateRepository(session_factory)
        user_repo = UserRepository(session_factory)
        tx_repo = TransactionRepository(session_factory)
        
        await state_repo.load_state()
        
        return user_repo, state_repo, tx_repo

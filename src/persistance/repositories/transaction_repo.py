from collections import deque
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import IntegrityError

from src.persistance.models import Transaction
from src.domain.events import TransferEvent

class TransactionRepository:
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory
        self._seen_txs = deque(maxlen=1000)

    async def exists(self, tx_hash: str) -> bool:
        if tx_hash in self._seen_txs:
            return True
        
        async with self._session_factory() as session:
            query = select(Transaction.id).where(Transaction.tx_hash == tx_hash).limit(1)
            result = await session.execute(query)
            is_exist = result.first() is not None
            
            if is_exist:
                self._seen_txs.append(tx_hash)
                
            return is_exist

    async def save(self, event: TransferEvent):
        self._seen_txs.append(event.tx_hash)

        async with self._session_factory() as session:
            try:
                tx_model = Transaction(
                    tx_hash=event.tx_hash,
                    from_address=event.sender,
                    to_address=event.receiver,
                    value=event.value,
                    symbol=event.symbol
                )
                
                session.add(tx_model)
                await session.commit()
                
            except IntegrityError:
                await session.rollback()
                print(f"⚠️ Transaction {event.tx_hash} already exists in DB")
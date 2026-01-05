from src.domain.events import EventManager, TransferEvent
from src.domain.events.base import Event
from src.persistance.repositories import TransactionRepository

class TransactionService:
    
    def __init__(
        self,
        event_manager: EventManager,
        transaction_repository: TransactionRepository
    ):
        self._event_manager = event_manager
        self._transaction_repository = transaction_repository
        
    async def _notify(self, event: Event):
        await self._event_manager.notify(event)        
        
    async def handle_crypto_event(self, event: TransferEvent):
        if not (await self._transaction_repository.exists(event.tx_hash)):
            await self._transaction_repository.save(event)
        
            if event.value > 100000:
                await self._notify(event)
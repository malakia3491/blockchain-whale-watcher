from .crypto import CryptoEventListener
from src.domain import TransactionService
from src.domain.events import CryptoEventFactory
from src.persistance.repositories import StateRepository, TransactionRepository

class BlockchainListenerRunner:
    
    def __init__(
        self,
        transaction_service: TransactionService,
        crypto_listener: CryptoEventListener,
        event_factory: CryptoEventFactory,
        app_state_repository: StateRepository,

    ):
        self._transaction_service = transaction_service
        self._crypto_listener = crypto_listener
        self._event_factory = event_factory
        self._app_state_repository = app_state_repository
        
    async def start(self):
        last_processed_block_from_db = self._app_state_repository.get_last_block()
        async for events, current_block_in_loop in self._crypto_listener.log_loop(start_block=last_processed_block_from_db):
            for crypto_event in events:
                event = self._event_factory.create_transfer_event(crypto_event)
                await self._transaction_service.handle_crypto_event(event)
           
            await self._app_state_repository.set_last_block(current_block_in_loop)
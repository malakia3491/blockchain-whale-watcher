import asyncio
from web3 import AsyncWeb3, AsyncHTTPProvider
from aiogram import Bot, Dispatcher

from src.persistance.repositories import UserRepository, TransactionRepository, StateRepository

from .sending.telegram.messanger import TelegramNotificationService
from .sending.telegram import TelegramInitializer

from src.domain import TransactionService, Config
from src.domain.events import EventManager, CryptoEventFactory, TransferEvent

from .crypto import CryptoEventListener
from .sending import TestMessanger
from .runner import BlockchainListenerRunner

class AppInitializer:
    def __init__(self, config: Config):
        self._config = config
    
    async def initialize(
        self,
        user_repo: UserRepository,
        app_state_repo: StateRepository,
        transaction_repo: TransactionRepository,
    ) -> tuple[BlockchainListenerRunner, Dispatcher, Bot]:     
        connection, contract = await self._initialize_event_filter(self._config)     
         
        tg_ini = TelegramInitializer(self._config)
        dispatcher, bot, messanger = tg_ini.initialize(user_repositry=user_repo)
      
        event_manager = self._initialize_event_manager(listeners=[TestMessanger(), messanger])
        event_factory = CryptoEventFactory()
        
        transaction_service = TransactionService(
            event_manager=event_manager,
            transaction_repository=transaction_repo,
        )
        
        crypto_listener = CryptoEventListener(
            poll_interval=12,
            connection=connection,
            contract=contract,
        )
        runner = BlockchainListenerRunner(
            transaction_service=transaction_service,
            crypto_listener=crypto_listener,
            event_factory=event_factory,
            app_state_repository=app_state_repo,
        )
        
        return runner, dispatcher, bot
        
    def _initialize_event_manager(self, listeners: list) -> EventManager:
        event_manager = EventManager()        
        for listener in listeners:                    
            event_manager.subscribe(TransferEvent, listener)
        return event_manager            
        
    async def _initialize_event_filter(self, config: Config):
        w3 = AsyncWeb3(AsyncHTTPProvider(config.node_url))
        
        if not await w3.is_connected():
            print(f"No connection with the node {config.node_url}")
            return

        contract = w3.eth.contract(address=config.target_contract, abi=config.erc_20_abi)
        return w3, contract
    
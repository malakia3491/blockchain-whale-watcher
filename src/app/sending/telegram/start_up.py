from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.domain.config import Config
from src.domain.messanger.base.handler import Handler
from src.persistance.repositories import UserRepository
from .messanger import TelegramNotificationService
from .messanger.Handlers import StartHandler

class TelegramInitializer:
    def __init__(self, config: Config):
        self._config = config
        
    def initialize(self, user_repositry: UserRepository):
        main_router = Router()
        handlers = self._initialize_handlers(user_repositry)
        for handler in handlers:            
            main_router.include_router(handler.router)
        
        bot = Bot(token=self._config.tg_api_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))    
        
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(main_router)            

        messanger = TelegramNotificationService(
            bot=bot,
            user_repo=user_repositry,
        )
        return dp, bot, messanger
        
    def _initialize_handlers(self, user_repositry: UserRepository) -> list[Handler]:
        start_handler = StartHandler(user_repo=user_repositry)
        return [start_handler]
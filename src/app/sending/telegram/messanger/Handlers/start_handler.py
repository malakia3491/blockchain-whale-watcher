from aiogram import F, types, Router

from src.persistance.repositories import UserRepository

class StartHandler:
    def __init__(self, user_repo: UserRepository):
        self.router = Router()
        self._user_repo = user_repo
        self._register_handlers()
    
    def _register_handlers(self):
        self.router.message.register(self.cmd_start, F.text == '/start')
    
    async def cmd_start(self, message: types.Message):
        await self._user_repo.add_user(message.chat.id)
        await message.answer("You are subscribed to recruitment notifications! 🐋")
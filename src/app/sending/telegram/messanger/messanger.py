from aiogram import Bot

from src.domain.events.base import Event, EventHandler
from src.persistance.repositories import UserRepository

class TelegramNotificationService(EventHandler):
    def __init__(self, bot: Bot, user_repo: UserRepository):
        self._bot = bot
        self._user_repo = user_repo

    async def handle(self, event: Event):
        msg = event.get_message_text()
        chat_ids = await self._user_repo.get_all_ids()
        for chat_id in chat_ids:
            try:
                await self._bot.send_message(chat_id=chat_id, text=msg)
            except Exception as e:
                print(f"Failed to send to {chat_id}: {e}")
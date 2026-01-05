import asyncio

from src.domain.events.base import Event, EventHandler

class TestMessanger(EventHandler):
    
    async def handle(self, event: Event):
        print(event.get_message_text())    
        await asyncio.sleep(1)
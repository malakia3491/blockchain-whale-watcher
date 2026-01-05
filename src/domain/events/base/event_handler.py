import abc

from .event import Event 

class EventHandler(abc.ABC):
    
    @abc.abstractmethod
    async def handle(self, event: Event):
        pass    
from src.domain.events.base import Event, EventHandler

class EventManager:
    _listeners: dict[str, list[EventHandler]] = {}
    
    def subscribe(self, event_type: type, listener: EventHandler):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: type, listener: EventHandler):
        if event_type not in self._listeners:
            raise ValueError("It does not containe the key")
        
        self._listeners[event_type].remove(listener)
                                           
    async def notify(self, event: Event):
        event_type = type(event)
        if event_type not in self._listeners:
            return 
        
        for listener in self._listeners[event_type]:
            await listener.handle(event)   
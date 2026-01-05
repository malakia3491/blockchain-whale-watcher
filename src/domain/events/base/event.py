import abc

class Event(abc.ABC):
    
    @abc.abstractmethod
    def get_message_text(self):
        pass    
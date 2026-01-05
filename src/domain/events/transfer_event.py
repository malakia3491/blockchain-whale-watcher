from .base import Event

class TransferEvent(Event):
    def __init__(
        self,
        tx_hash: str,
        symbol: str,
        sender: str,
        reciever: str,
        value: float,
    ):
        self._data = {
           "tx_hash": tx_hash,
           "symbol": symbol,
           "sender": sender,
           "receiver": reciever,
           "value": value,    
        }
    
    @property
    def data(self) -> dict:
        return self._data

    @property
    def tx_hash(self):
        return self._data['tx_hash']
    
    @property
    def symbol(self):
        return self._data['symbol']
    
    @property
    def sender(self):
        return self._data['sender']
    
    @property
    def receiver(self):
        return self._data['receiver']
    
    @property
    def value(self):
        return self._data['value']
    
    def get_message_text(self):
        msg = (
            f"🐋 <b>WHALE ALERT</b>\n"
            f"💰 Value: {self.value:,.2f} USDT\n"
            f"📤 From: <code>{self.sender}</code>\n"
            f"📥 To: <code>{self.receiver}</code>"
        )
        return msg
from src.domain.events import TransferEvent

class CryptoEventFactory:
    
    def create_transfer_event(self, crypto_event: dict):
        tx_hash = crypto_event['transactionHash'].hex()
        sender = crypto_event['args']['from']
        receiver = crypto_event['args']['to']
        value = crypto_event['args']['value'] / 10**6
        
        event = TransferEvent(
            tx_hash=tx_hash,
            symbol="USDT",
            sender=sender,
            reciever=receiver,
            value=value,
        )
        
        return event
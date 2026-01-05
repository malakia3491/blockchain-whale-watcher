import asyncio

class CryptoEventListener:    
    def __init__(
        self,
        connection,
        contract,
        poll_interval: int,
    ):
        self._connection = connection
        self._contract = contract 
        self._poll_interval = poll_interval

    async def log_loop(self, start_block: int):
        last_processed_block = start_block if start_block else await self._connection.eth.block_number
        while True:
            try:
                current_block = await self._connection.eth.block_number
                if current_block > last_processed_block:                    
                    events = await self._contract.events.Transfer.get_logs(
                        from_block=last_processed_block + 1,
                        to_block=current_block
                    )
                    last_processed_block = current_block

                    yield events, last_processed_block
                await asyncio.sleep(self._poll_interval)                    
            except Exception as e:
                print(f"Connection error: {e}")
import os
import asyncio

from src.app import AppInitializer
from src.persistance import DbInitializator
from src.domain import Config

async def main():
    config = Config(os.path.abspath("ini.conf"))
    app_ini = AppInitializer(config)
    db_ini = DbInitializator(config)
    user_repo, state_repo, ts_repo = await db_ini.initialize()
    blockchain_runner, dispatcher, bot = await app_ini.initialize(
        user_repo=user_repo,
        app_state_repo=state_repo,
        transaction_repo=ts_repo,
    )
    
    await asyncio.gather(
        blockchain_runner.start(),
        dispatcher.start_polling(bot)            
    )

if __name__ == "__main__":
    asyncio.run(main())
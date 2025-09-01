import asyncio
from app.bot import bot
from app.db import init_db

async def main():
    # Step 1: Init database
    await init_db()

    # Step 2: Start bot
    print("Bot is starting...")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main())

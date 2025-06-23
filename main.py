import asyncio
from code.quotex_bot import QuotexSignalBot

if __name__ == "__main__":
    bot = QuotexSignalBot(token="YOUR_TELEGRAM_BOT_TOKEN")
    asyncio.run(bot.run())

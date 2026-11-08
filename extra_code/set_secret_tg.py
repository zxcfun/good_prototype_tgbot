import asyncio
from aiogram import Bot
from config import settings

async def main():

    bot = Bot(token=settings.BOT_TOKEN)
    url = settings.TELEGRAM_WEBHOOK_URL
    secret = settings.TELEGRAM_WEBHOOK_SECRET

    await bot.set_webhook(url=url, secret_token=secret, drop_pending_updates=True)
    print(f"Вебхук успешно установлен на {url}")

    # Проверяем, что установилось
    info = await bot.get_webhook_info()
    print(f"Текущий статус: {info.url}")

if __name__ == "__main__":
    asyncio.run(main())
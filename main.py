import asyncio
from aiogram import Bot, Dispatcher

from handlers import router


bot = Bot('6941678011:AAFHog6xvh4YN1BV7p3vli3hhHKRoU_E0kw')
dp = Dispatcher()
dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

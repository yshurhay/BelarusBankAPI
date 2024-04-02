import sys

import aiohttp
import asyncio
import pandas as pd
from aiohttp import ContentTypeError
from aiogram import Bot, Dispatcher

from handlers import router

ALPHABET = 'йцукенгшщзхъфывапролджэячсмитьбюё'


async def get_info(count):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://belarusbank.by/api/news_info?lang=ru') as response:
                text = await response.json()

                if count > len(text) or count <= 0:
                    return False

                return [{
                    'title': text[i]['name_ru'],
                    'text': text[i]['html_ru'],
                    'date': text[i]['start_date']
                }
                    for i in range(count)]
    except ContentTypeError:
        print('Not correct url')
        sys.exit()


def find_max_count(all_info):
    text = ''.join(info['text'] for info in all_info)
    maximum = {}
    for letter in ALPHABET:
        maximum[letter] = text.lower().count(letter)
    return max(maximum.items(), key=lambda x: x[1])


bot = Bot('6941678011:AAFHog6xvh4YN1BV7p3vli3hhHKRoU_E0kw')
dp = Dispatcher()
dp.include_router(router)


async def main():
    # all_news = await get_info()
    # even_month = list(filter(lambda x: int(x['date'][5:7]) % 2, all_news))
    # max_letter_count = find_max_count(all_news)
    #
    # task_3 = {
    #     'text_max_length': max(all_news, key=lambda x: len(x['text'])),
    #     'article_max_length': max(all_news, key=lambda x: len(x['title'].split()))['title'],
    #     max_letter_count[0]: max_letter_count[1]
    # }
    #
    # df1 = pd.DataFrame(all_news)
    # df2 = pd.DataFrame(even_month)
    # df3 = pd.DataFrame(task_3)
    # to_excel(df1, df2, df3)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

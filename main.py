import sys

import aiohttp
import asyncio
import pandas as pd
from aiohttp import ContentTypeError

ALPHABET = 'йцукенгшщзхъфывапролджэячсмитьбюё'


async def get_info():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://belarusbank.by/api/news_info?lang=ru') as response:
                text = await response.json()
                return [{
                    'title': text[i]['name_ru'],
                    'text': text[i]['html_ru'],
                    'date': text[i]['start_date']
                }
                    for i in range(20)]
    except ContentTypeError:
        print('Not correct url')
        sys.exit()


def find_max_count(all_info):
    text = ''.join(info['text'] for info in all_info)
    maximum = {}
    for letter in ALPHABET:
        maximum[letter] = text.lower().count(letter)
    return max(maximum.items(), key=lambda x: x[1])


def to_excel(*items):
    with pd.ExcelWriter('output.xlsx') as writer:
        for i, item in enumerate(items):
            item.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)


async def main():
    all_news_info = await get_info()
    even_month_info = list(filter(lambda x: int(x['date'][5:7]) % 2, all_news_info))
    max_letter_count = find_max_count(all_news_info)
    print(max_letter_count)
    task_3_info = {
        'text_max_length': max(all_news_info, key=lambda x: len(x['text'])),
        'article_max_length': max(all_news_info, key=lambda x: len(x['title'].split()))['title'],
        max_letter_count[0]: max_letter_count[1]
    }

    df1 = pd.DataFrame(all_news_info)
    df2 = pd.DataFrame(even_month_info)
    df3 = pd.DataFrame(task_3_info)
    to_excel(df1, df2, df3)


if __name__ == '__main__':
    asyncio.run(main())
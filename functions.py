import aiohttp
import pandas as pd
from aiohttp import ContentTypeError


async def get_info(count):
    """Get API and convert to list[dict]"""

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://belarusbank.by/api/news_info?lang=ru') as response:
                text = await response.json()

                if count > len(text) or count <= 0:
                    return 'Введите число'

                return [{
                    'title': text[i]['name_ru'],
                    'text': text[i]['html_ru'],
                    'date': text[i]['start_date']
                }
                    for i in range(count)]
    except ContentTypeError:
        return 'Not correct url'


def to_excel(item, name):
    """Write dict to excel"""

    try:
        item_db = pd.DataFrame(item)
        item_db.to_excel(f'{name}.xlsx')
    except ValueError:
        print('Not correct writing to excel')

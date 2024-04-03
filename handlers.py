from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from functions import get_info, to_excel

import keyboards as kb


router = Router()
all_news = []


class News(StatesGroup):
    count = State()


class Count(StatesGroup):
    symbol = State()


@router.message(F.text.lower() == 'самый длинный текст')
async def text(message: Message):
    """Find the longest text and send excel file"""

    longest_text = max(all_news, key=lambda x: len(x['text']))
    to_excel({'text_max_length': longest_text}, 'longest_text')
    await message.answer_document(FSInputFile('longest_text.xlsx', filename='longest_text.xlsx'), reply_markup=kb.main_kb)


@router.message(F.text.lower() == 'самый длинный заголовок')
async def text(message: Message):
    """Find the longest title and send excel file"""

    longest_title = max(all_news, key=lambda x: len(x['title'].split()))
    to_excel({'title_max_length': longest_title}, 'longest_title')
    await message.answer_document(FSInputFile('longest_title.xlsx', filename='longest_title.xlsx'), reply_markup=kb.main_kb)


@router.message(F.text.lower() == 'количество символов')
async def text(message: Message, state: FSMContext):
    """Set state with any symbol"""

    await state.set_state(Count.symbol)
    await message.answer('Введите символ')


@router.message(Count.symbol)
async def symbol(message: Message, state: FSMContext):
    """Find symbol count in text and send info"""

    await state.update_data(symbol=message.text)
    data = await state.get_data()
    all_text = ' '.join(news['text'] for news in all_news)
    await message.answer(f'Количество "{data['symbol']}" в тексте: {all_text.count(data['symbol'])}')


@router.message(or_f(F.text.lower() == 'получить новости', CommandStart()))
async def get_news(message: Message, state: FSMContext):
    """Set state with news count"""

    await state.set_state(News.count)
    await message.answer('Введи количество новостей')


@router.message(News.count)
async def count(message: Message, state: FSMContext):
    """Get first n count news and send excel file"""

    try:
        global all_news
        result = await get_info(int(message.text))
        if isinstance(result, str):
            await message.answer(result)
        else:
            await state.update_data(count=int(message.text))
            to_excel(result, 'news')
            all_news = result
            await message.answer_document(FSInputFile('news.xlsx', filename='news.xlsx'), reply_markup=kb.main_kb)
    except ValueError:
        await message.answer('Введите число')

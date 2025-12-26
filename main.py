
import logging
from io import BytesIO
from aiogram import Bot,Dispatcher,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ContentType

from config import TELEGRAM_BOT_TOKEN,STATE_TTL_SECONDS
from keyboards import timeframe_keyboard
from state import TTLState
from predictor import analyze

state=TTLState(STATE_TTL_SECONDS)

async def start(m:Message):
    await m.answer("Пришли скрин графика, затем выбери таймфрейм")

async def image(m:Message):
    bio=BytesIO()
    if m.photo:
        f=await m.bot.get_file(m.photo[-1].file_id)
        await m.bot.download_file(f.file_path,bio)
    else:
        f=await m.bot.get_file(m.document.file_id)
        await m.bot.download_file(f.file_path,bio)
    await state.set(m.from_user.id,"img",bio.getvalue())
    await m.answer("Выбери таймфрейм",reply_markup=timeframe_keyboard())

async def tf(cb:CallbackQuery):
    img=await state.get(cb.from_user.id,"img")
    res=analyze(img)
    if res is None:
        await cb.message.answer("Скрин нечитабелен")
    else:
        await cb.message.answer(f"Вероятность роста 2–3 свечи: {int(res*100)}%\nНе фин. совет")
    await state.clear(cb.from_user.id)
    await cb.answer()

def main():
    logging.basicConfig(level=logging.INFO)
    bot=Bot(TELEGRAM_BOT_TOKEN)
    dp=Dispatcher()
    dp.message.register(start,CommandStart())
    dp.message.register(image,F.content_type.in_({ContentType.PHOTO,ContentType.DOCUMENT}))
    dp.callback_query.register(tf,F.data.startswith("tf:"))
    dp.run_polling(bot)

if __name__=="__main__":
    main()

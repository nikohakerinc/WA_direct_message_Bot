import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

start_message = '''Привет \U0001F44B
Данный бот позволяет начать общение с пользователем WhatsApp не добавляя в контакты его номер телефона
Выберите язык:

Hello \U0001F44B
This bot allows you to start a conversation with a WhatsApp user without adding their phone number to your contacts.
Choose your language:'''

# Создаем клавиатуру выбора языка
language_keyboard = InlineKeyboardMarkup(row_width=1)
language_keyboard.add(
    InlineKeyboardButton(" 🇷🇺 Продолжить на русском", callback_data="lang_ru"),
    InlineKeyboardButton(" 🇬🇧 Continue in English", callback_data="lang_en"),
)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(start_message, reply_markup=language_keyboard)

# Обработчик нажатия кнопок выбора языка
@dp.callback_query_handler(lambda query: query.data.startswith("lang_"))
async def language_callback(callback_query: types.CallbackQuery, state: FSMContext):
    lang = callback_query.data.split("_")[1]
    await state.update_data(lang=lang)  # Сохраняем значение lang в состоянии
    if lang == "ru":
        await callback_query.answer("Выбран русский язык")
        await callback_query.message.edit_text('Введите номер телефона пользователя WhatsApp в любом формате')
    elif lang == "en":
        await callback_query.answer("English language selected")
        await callback_query.message.edit_text('Enter the WhatsApp user phone number in any format')

# Обработчик сообщения с телефоном от пользователя
@dp.message_handler()
async def process_phone_number(message: types.Message, state: FSMContext):
    # Получаем значение lang из состояния
    data = await state.get_data()
    lang = data.get('lang')
    # Удаляем все нецифровые символы из сообщения
    phone_number = re.sub(r'\D', '', message.text)
    if not phone_number.isdigit():
        if lang == "ru":
            await message.reply('Введённые вами данные не похожи на номер телефона\U0001F914\nВведите номер телефона пользователя WhatsApp в любом формате')
        elif lang == "en":
            await message.reply('The information you entered does not look like a phone number\U0001F914\nEnter the WhatsApp user phone number in any format')
    else:
        if len(phone_number) < 10 or len(phone_number) > 15:
            if lang == "ru":
                await message.reply('Вы ввели некорректный номер телефона')
            elif lang == "en":
                await message.reply('You entered an incorrect phone number')
        else:
            wa_link = f'https://wa.me/{phone_number}'
            keyboard = InlineKeyboardMarkup(row_width=1)
            if lang == "ru":
                keyboard.add(
                    InlineKeyboardButton("Перейти по ссылке", url=wa_link),
                )
                await message.answer(f'Ваша ссылка для чата с пользователем WhatsApp\n{wa_link}', reply_markup=keyboard, disable_web_page_preview=True)
            elif lang == "en":
                keyboard.add(
                    InlineKeyboardButton("Go to link", url=wa_link),
                )
                await message.answer(f'Your direct link for chatting with WhatsApp user\n{wa_link}', reply_markup=keyboard, disable_web_page_preview=True)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
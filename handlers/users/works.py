import logging
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
import aioschedule
import asyncio
import keybords.inline.choice_buttons as key
import keybords.inline.callback_datas as call_datas
from bd.sql import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import erp

# Кнопка старт, аутентифицирует человека, отправляет клавиатуру
@dp.message_handler(Command('start'))
async def show_menu(message: Message):
    text = '''🤝 Если ты здесь, значит точно уверен, что PR — дело общее! 

На 2023 год у нас есть для тебя много классных миссий, выполняя которые ты можешь получить баллы в свою копилку и обменять их на крутой мерч.'''
    await message.answer(text, reply_markup=key.menu_keyboard)
    response = await erp.get_id_erp(message.from_user.id)
    await create_profile(message.from_user.id, response[0], response[1])

# Кнопка для Приветствия
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='next'))
async def helo_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    emp = (await sel_emploes(call.message.chat.id))[0][0]
    await call.message.edit_text(f'Ты в команде, {emp} 😎\nПриступим к выполнению миссий', reply_markup=key.helo_keyboard)
    await call.answer()
    
# Кнопка для помощи
@dp.callback_query_handler(call_datas.helo_callback.filter(item_helo='helo'))
async def helo_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text(f'Перед тобой список миссий за которые ты получишь 💎\nВыполняй их в любом порядке, а если захочешь посмотреть количество баллов, жми кнопку «Мои баллы»', reply_markup=key.mission_keyboard)
    await call.answer()

# Кнопка миссии
@dp.callback_query_handler(call_datas.mission_callback.filter(item_mission='miss'))
async def mission_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    bal = (await check_point(call.message.chat.id))[0][0]
    await call.message.edit_text(f'У тебя сейчас {bal} 💎')
    await call.answer()

# Кнопка мои баллы
@dp.callback_query_handler(call_datas.mission_callback.filter(item_mission='my_bolls'))
async def my_bolls_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    bal = (await check_point(call.message.chat.id))[0][0]
    await call.message.edit_text(f'У тебя сейчас {bal} 💎', reply_markup=key.back_keyboard)
    await call.answer()

# Кнопка назад
@dp.callback_query_handler(call_datas.back_callback.filter(item_back='back'))
async def back_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text(f'Перед тобой список миссий за которые ты получишь 💎\nВыполняй их в любом порядке, а если захочешь посмотреть количество баллов, жми кнопку «Мои баллы»', reply_markup=key.mission_keyboard)
    await call.answer()
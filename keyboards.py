from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def one_five_answer_kb():
    kb = [
        [
            types.KeyboardButton(text='1'),
            types.KeyboardButton(text='2'),
            types.KeyboardButton(text='3'),
            types.KeyboardButton(text='4'),
            types.KeyboardButton(text='5')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Оцените ответ от 1 до 5'
    )
    return keyboard


def one_five_service_kb():
    kb = [
        [
            types.KeyboardButton(text='1'),
            types.KeyboardButton(text='2'),
            types.KeyboardButton(text='3'),
            types.KeyboardButton(text='4'),
            types.KeyboardButton(text='5')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Оцените сервис от 1 до 5'
    )
    return keyboard
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.dice_emoji import DiceEmoji
import re
import json
import pickle
#import sklearn
from sklearn.linear_model import LogisticRegression
from keyboards import one_five_answer_kb, one_five_service_kb


logging.basicConfig(level=logging.INFO)
bot = Bot(token="<123456790:YOUR_BOT_TOKEN>")
dp = Dispatcher()


def get_iris_type(user_request):
  iris_type_dict = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
  return iris_type_dict[lr_new.predict(user_request)[0]]


class PredictonProcces(StatesGroup):
    entering_data = State()
    getting_prediction_rate = State()
    entering_service_rate = State()


async def main():
    await dp.start_polling(bot)


def load_json(filename):
    with open(filename, 'r') as json_file:
        dict_from_file = json.load(json_file)
    return dict_from_file


def user_stat_init(user_id, user_name, user_stat_dict):
    user_stat_dict[str(user_id)] = {'username': str(user_name), 'req_count' : 0, 'rate_count' : 0, 'rate_sum': 0, 'rate_avg' : 0, 'service_rate': 0}
    return None


def user_stat_update(user_stat_dict):
    with open('user_stat.json', 'w') as user_stat_file:
        json.dump(user_stat_dict, user_stat_file)
    return None


@dp.message(Command(commands=['kubik']))
async def cmd_kubik(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@dp.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    if user_data_dict.get(str(message.from_user.id)) == None:
        user_stat_init(message.from_user.id, message.from_user.username, user_data_dict)
    else:
        pass
    await message.answer(
        text=f'''Привет {message.from_user.id, message.from_user.username}! Этот бот помогает определить тип цветка ириса.
Вам доступны функции:
Получение прогноза по данным вашего цветка /start_prediction
Ваша статистика /my_stat
Общая статистика /stat
Оценка сервиса /service_rate
Выкатить кубик /kubik''', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)


@dp.message(StateFilter(None), Command("start_prediction"))
async def cmd_start_prediction(message: Message, state: FSMContext):
    await message.answer(
        text='Пожалуйста, введите через пробел длину чашелистника, ширину чашелистника, длину лепестка, ширину лепестка. Например, так: 5.1 3.0 1.4 0.2')
    await state.set_state(PredictonProcces.entering_data)


@dp.message(StateFilter(PredictonProcces.entering_data))
async def cmd_process_prediction(message: Message, state: FSMContext):
    global user_data_dict
    msg_text = message.text
    if re.match(r'\d+.\d+\s\d+.\d+\s\d+.\d+\s\d+.\d+', message.text) == None:
        await message.answer(text='Введенные данные не соотвестуют формату. Пожалуйста, введите через пробел длину чашелистника, ширину чашелистника, длину лепестка, ширину лепестка. Например, так: 5.1 3.0 1.4 0.2')
    else:
        prediction = get_iris_type([[float(el) for el in msg_text.split()]])
        if user_data_dict.get(str(message.from_user.id)) == None:
            user_stat_init(message.from_user.id, message.from_user.username, user_data_dict)
        else:
            pass
        user_data_dict[str(message.from_user.id)]['req_count'] += 1
        user_stat_update(user_data_dict)
        await state.set_state(PredictonProcces.getting_prediction_rate)
        await message.answer(
            text=f'Ваш цветок похож на вид ириса {prediction}. Пожалуйста, оцените предсказание от 1 до 5.', reply_markup=one_five_answer_kb())


@dp.message(StateFilter(PredictonProcces.getting_prediction_rate))
async def cmd_entering_prediction_rate(message: Message, state: FSMContext):
    global user_data_dict
    if message.text in (str(i) for i in range(1,6)):
        user_data_dict[str(message.from_user.id)]['rate_count'] += 1
        user_data_dict[str(message.from_user.id)]['rate_sum'] += int(message.text)
        user_data_dict[str(message.from_user.id)]['rate_avg'] = user_data_dict[str(message.from_user.id)]['rate_sum']/user_data_dict[str(message.from_user.id)]['rate_count']
        user_stat_update(user_data_dict)
        await state.set_state(None)
        await message.answer(
            text=f'Ваша оценка {message.text} успешно записана!', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(
            text='Введено неверное значение. Пожалуйста, попробуйте ещё раз или можете выйти при помощи /start.',
            reply_markup=one_five_answer_kb())


@dp.message(StateFilter(None), Command('service_rate'))
async def cmd_service_rate(message: Message, state: FSMContext):
    await state.set_state(PredictonProcces.entering_service_rate)
    await message.answer(
        text=f'Пожалуйста, оцените сервис от 1 до 5.',
        reply_markup=one_five_service_kb())

@dp.message(StateFilter(PredictonProcces.entering_service_rate))
async def cmd_service_rate_enter(message: Message, state: FSMContext):
    global user_data_dict
    if message.text in (str(i) for i in range(1,6)):
        if user_data_dict.get(str(message.from_user.id)) == None:
            user_stat_init(message.from_user.id, message.from_user.username, user_data_dict)
            user_data_dict[str(message.from_user.id)]['service_rate'] = int(message.text)
            user_stat_update(user_data_dict)
        else:
            user_data_dict[str(message.from_user.id)]['service_rate'] = int(message.text)
            user_stat_update(user_data_dict)
        await state.set_state(None)
        await message.answer(
            text=f'Ваша оценка {message.text} успешно записана!', reply_markup=types.ReplyKeyboardRemove())

    else:
        await message.answer(
            text=f'Введено неверное значение. Пожалуйста, попробуйте ещё раз или можете выйти при помощи /start.',
            reply_markup=one_five_service_kb())


@dp.message(Command('my_stat'))
async def cmd_my_stat(message: Message):
    global user_data_dict
    await message.answer(
        text=f'''Ваша статистика:
Имя в telegram: {user_data_dict[str(message.from_user.id)]['username']}
id: {message.from_user.id}
Количество запросов для цветков: {user_data_dict[str(message.from_user.id)]['req_count']}
Количество оценок результатов: {user_data_dict[str(message.from_user.id)]['rate_count']}
Средняя оценка результатов запросов: {user_data_dict[str(message.from_user.id)]['rate_avg']}
Оценка сервиса: {'Отсутствует' if user_data_dict[str(message.from_user.id)]['service_rate']==0 else user_data_dict[str(message.from_user.id)]['service_rate']}

К оглавлению: /start''', reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command('stat'))
async def cmd_my_stat(message: Message):
    global user_data_dict
    req_all = 0
    rate_count_all = 0
    rate_sum_all = 0
    service_rate_sum = 0
    sevice_rate_count = 0
    for el in user_data_dict:
        req_all +=  user_data_dict[el]['req_count']
        rate_count_all += user_data_dict[el]['rate_count']
        rate_sum_all += user_data_dict[el]['rate_sum']
        service_rate_sum += user_data_dict[el]['service_rate']
        sevice_rate_count = (sevice_rate_count+1) if user_data_dict[el]['service_rate']!=0 else sevice_rate_count
    await message.answer(
        text=f'''Общая статистика:
Количество пользователей: {len(user_data_dict)}
Количество запросов для цветков: {req_all}
Количество оценок запросов: {rate_count_all}
Средняя оценка результатов запросов: {'Отсутствует' if rate_count_all == 0 else rate_sum_all/rate_count_all}
Средняя оценка сервиса: {'Отсутствует' if sevice_rate_count == 0 else service_rate_sum/sevice_rate_count}

К оглавлению: /start''', reply_markup=types.ReplyKeyboardRemove())


user_data_dict = load_json('user_stat.json')
with open('lr_trained.pickle', 'rb') as f:
    lr_new = pickle.loads(pickle.load(f))


if __name__ == "__main__":
    asyncio.run(main())
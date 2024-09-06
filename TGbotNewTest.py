import pytest
import aiogram
import asyncio
import pytest_asyncio
from unittest.mock import AsyncMock
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram import types
from keyboards import one_five_answer_kb, one_five_service_kb


from TGbotNew import cmd_process_prediction
from TGbotNew import PredictonProcces
from TGbotNew import cmd_kubik
from TGbotNew import cmd_start
from TGbotNew import cmd_start_prediction
from TGbotNew import cmd_entering_prediction_rate
from TGbotNew import cmd_service_rate
from TGbotNew import cmd_service_rate_enter


@pytest.mark.asyncio
async def test_cmd_process_prediction():
   messagemock = AsyncMock()
   messagemock.text = '123456789'
   await cmd_process_prediction(message=messagemock, state=PredictonProcces.entering_data)
   messagemock.answer.assert_called_with(**{'text':'Введенные данные не соотвестуют формату. Пожалуйста, введите через пробел длину чашелистника, ширину чашелистника, длину лепестка, ширину лепестка. Например, так: 5.1 3.0 1.4 0.2'})


@pytest.mark.asyncio
async def test_cmd_kubik():
   message_mock = AsyncMock()
   await cmd_kubik(message = message_mock)
   message_mock.answer_dice.assert_called_with(**{'emoji': DiceEmoji.DICE})


@pytest.mark.asyncio
async def test_cmd_start():
   message_mock = AsyncMock()
   message_mock.from_user.id = 12345
   message_mock.from_user.username = 'UserName'
   state_mock = AsyncMock()
   await cmd_start(message = message_mock, state=state_mock)
   state_mock.set_state.assert_called_with(None)
   message_mock.answer.assert_called_with(**{'text': f'''Привет {message_mock.from_user.id, message_mock.from_user.username}! Этот бот помогает определить тип цветка ириса.
Вам доступны функции:
Получение прогноза по данным вашего цветка /start_prediction
Ваша статистика /my_stat
Общая статистика /stat
Оценка сервиса /service_rate
Выкатить кубик /kubik''', 'reply_markup': types.ReplyKeyboardRemove()})


@pytest.mark.asyncio
async def test_cmd_start_prediction():
   message_mock = AsyncMock()
   state_mock = AsyncMock()
   await cmd_start_prediction(message = message_mock, state=state_mock)
   state_mock.set_state.assert_called_with(PredictonProcces.entering_data)
   message_mock.answer.assert_called_with(**{'text': 'Пожалуйста, введите через пробел длину чашелистника, ширину чашелистника, длину лепестка, ширину лепестка. Например, так: 5.1 3.0 1.4 0.2'})


@pytest.mark.asyncio
async def test_cmd_process_prediction_corr_inpt():
   messagemock = AsyncMock()
   messagemock.text = '1.2 3.4 5.6 7.8'
   state_mock = AsyncMock()
   await cmd_process_prediction(message=messagemock, state=state_mock)
   state_mock.set_state.assert_called_with(PredictonProcces.getting_prediction_rate)
   messagemock.answer.assert_called_with(**{'text': f'Ваш цветок похож на вид ириса virginica. Пожалуйста, оцените предсказание от 1 до 5.', 'reply_markup' : one_five_answer_kb()})


@pytest.mark.asyncio
async def test_cmd_entering_prediction_rate():
   messagemock = AsyncMock()
   messagemock.text = '100500'
   await cmd_entering_prediction_rate(message=messagemock, state=PredictonProcces.getting_prediction_rate)
   messagemock.answer.assert_called_with(**{'text': 'Введено неверное значение. Пожалуйста, попробуйте ещё раз или можете выйти при помощи /start.',
            'reply_markup' : one_five_answer_kb()})


@pytest.mark.asyncio
async def test_cmd_entering_prediction_rate_corr_inpt():
   messagemock = AsyncMock()
   messagemock.text = '5'
   messagemock.from_user.id = '12345'
   state_mock = AsyncMock()
   await cmd_entering_prediction_rate(message=messagemock, state=state_mock)
   messagemock.answer.assert_called_with(**{'text': f'Ваша оценка {messagemock.text} успешно записана!', 'reply_markup' : types.ReplyKeyboardRemove()})


@pytest.mark.asyncio
async def test_cmd_service_rate():
   message_mock = AsyncMock()
   state_mock = AsyncMock()
   await cmd_service_rate(message = message_mock, state=state_mock)
   state_mock.set_state.assert_called_with(PredictonProcces.entering_service_rate)
   message_mock.answer.assert_called_with(**{'text': f'Пожалуйста, оцените сервис от 1 до 5.', 'reply_markup' : one_five_service_kb()})


@pytest.mark.asyncio
async def test_cmd_service_rate_enter():
   messagemock = AsyncMock()
   messagemock.text = '100500'
   state_mock = AsyncMock()
   await cmd_service_rate_enter(message=messagemock, state=state_mock)
   messagemock.answer.assert_called_with(**{'text' : f'Введено неверное значение. Пожалуйста, попробуйте ещё раз или можете выйти при помощи /start.',
            'reply_markup' : one_five_service_kb()})


@pytest.mark.asyncio
async def test_cmd_service_rate_enter_corr_inpt():
   messagemock = AsyncMock()
   messagemock.text = '5'
   state_mock = AsyncMock()
   await cmd_service_rate_enter(message=messagemock, state=state_mock)
   state_mock.set_state.assert_called_with(None)
   messagemock.answer.assert_called_with(**{'text': f'Ваша оценка {messagemock.text} успешно записана!', 'reply_markup' : types.ReplyKeyboardRemove()})
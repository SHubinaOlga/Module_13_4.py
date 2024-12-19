from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Calories')
async def set_age(massage):
    await massage.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(massage, state):
    await state.update_data(age = massage.text)
    await massage.answer(f'Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(massage, state):
    await state.update_data(growth = massage.text)
    await massage.answer(f'Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(massage, state):
    await state.update_data(weight = massage.text)
    data = await state.get_data()

    men = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    women = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161

    await massage.answer(f' Ваша норма калорий в сутки: 1) Для женщин: {women} ккал, 2) Для мужчин: {men} ккал')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler(text=['/start'])
async def start_message(massage):
    print('Start message')
    await massage.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_massages(message):
    print('Сообщение!')
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
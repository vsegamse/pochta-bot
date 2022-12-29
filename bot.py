from aiogram import *
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API = '5741501602:AAHLLnuEMVc3HuNOpVeZQAnL0nWGWsYhqMc'

bot = Bot(API)
Tbot = Dispatcher(bot, storage=MemoryStorage())

d = 0
p = 0
k = 0

class States(StatesGroup):
	kv_in_p = State()

@Tbot.message_handler(commands=['start'])
async def start(msg):
	global d
	global p
	global k
	d = 0
	p = 0
	k = 0

	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	nd = types.KeyboardButton('Начать день')
	keyboard.add(nd)

	await msg.answer('👋')
	await msg.answer(f'Привет {msg.from_user.first_name}, я Почта-бот!\n\nЯ буду помогать тебе считать сколько домов, подъездов и квартир ты закончил!\n\nВперёд работать!', reply_markup=keyboard)

@Tbot.message_handler()
async def msgs(msg: types.Message):
	global d
	global p
	global k
	if msg.text == 'Начать день':
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		zd = types.KeyboardButton('Завершить дом')
		zp = types.KeyboardButton('Завершить подъезд')
		stats = types.KeyboardButton('Статистика')
		zday = types.KeyboardButton('Завершить день')
		keyboard.add(zd, zp, stats, zday)
		await msg.answer('👋')
		await msg.answer('Доброго времени суток! Вперёд работать, и удачи!', reply_markup=keyboard)
	elif msg.text == 'Завершить дом':
		d += 1
		await msg.answer(f'🏠Супер, дом завершён!')
	elif msg.text == 'Завершить подъезд':
		p += 1
		await msg.answer('🚪Отлично, подъезд завершён! Теперь напиши, сколько было квартир в этом подъезде (пример: 46-84)', reply_markup=types.ReplyKeyboardRemove())
		await	States.kv_in_p.set()
	elif msg.text == 'Статистика':
		await msg.answer(f'📈Ваша статистика за сегодня:\n\nДома: {d}\nПодъезды: {p}\nКвартиры: {k}')
	elif msg.text == 'Завершить день':
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		nd = types.KeyboardButton('Начать день')
		keyboard.add(nd)
		await msg.answer(f'✅День закончен!\n\nСтатистика за этот день:\n\nДома: {d}\nПодъезды: {p}\nКвартиры: {k}', reply_markup=keyboard)
		d = 0
		p = 0
		k = 0

@Tbot.message_handler(state=States.kv_in_p)
async def kvs(msg: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	zd = types.KeyboardButton('Завершить дом')
	zp = types.KeyboardButton('Завершить подъезд')
	stats = types.KeyboardButton('Статистика')
	zday = types.KeyboardButton('Завершить день')
	keyboard.add(zd, zp, stats, zday)

	global k
	kvartiry = msg.text.split(sep='-')
	await msg.answer(f'Замечательно! В этом подъезде было {int(kvartiry[1]) - int(kvartiry[0]) + 1} квартир', reply_markup=keyboard)
	k += int(kvartiry[1]) - int(kvartiry[0]) + 1
	await States.previous()

if __name__ == '__main__':
	executor.start_polling(Tbot)
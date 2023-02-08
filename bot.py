import asyncio

from aiogram import Bot, Dispatcher, executor, types
import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import sqlite3, json

TOKEN = '5805654592:AAHHtRMKdutlPEqfubz6jVbUVoK-0SBkJ0k'

conn = sqlite3.connect('flags.db', check_same_thread=False)
cursor = conn.cursor()

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

# def add_new_user_to_db(tg_id):
#     user = cursor.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
#     if user.fetchone() is None:
#         cursor.execute('INSERT INTO users (tg_id, state) VALUES (?, ?)', (tg_id, None))
#         conn.commit()
#     return

# def change_user_state(tg_id, state):
#     cursor.execute('UPDATE users SET state = ? WHERE tg_id = ?', (state, tg_id,))
#     return

class ClientStatesGroup(StatesGroup):
    in_menu = State()
    inviting = State()
    confirmation = State()
    round1 = State()
    round2 = State()
    round3 = State()
    round4 = State()
    round5 = State()
    finished_answer = State()


def get_keyboard(host_id):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text='Готов', callback_data=f'is_ready_to_fight_with_{host_id}'))
    kb.add(InlineKeyboardButton(text='Не готов', callback_data=f'is_ready_not_to_fight_with_{host_id}'))
    return kb


def get_end_match_kb():
    kb = ReplyKeyboardMarkup()
    kb.add(KeyboardButton(text='Завершить матч'))
    return kb


def go_keyboard():
    kb = ReplyKeyboardMarkup()
    kb.add(KeyboardButton(text='Начать матч'))
    return kb


def get_answers_keyboard(answers):
    kb = ReplyKeyboardMarkup(row_width=2)
    buttons = []
    for answer in answers:
        btn = KeyboardButton(text=f'{answer}')
        buttons.append(btn)
    kb.add(*buttons)
    return kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    # add_new_user_to_db(message.chat.id)
    await message.delete()
    await ClientStatesGroup.in_menu.set()
    msg = await bot.send_message(chat_id=message.chat.id, text=f"Привет, твой id: {message.chat.id}")
    async with state.proxy() as data:
        data['last_bot_msg_id'] = msg.message_id



@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    # change_user_state(message.chat, 'in_menu')
    await message.delete()
    await bot.send_message(chat_id=message.chat.id, text="Состояние сброшено")
    await state.finish()



@dp.message_handler(commands=['create_room'], state=ClientStatesGroup.in_menu)
async def create_room(message: types.Message, state: FSMContext):
    await message.delete()
    msg = await bot.send_message(chat_id=message.chat.id, text=f"Введите id соперника")
    async with state.proxy() as data:
        data['last_bot_msg_id'] = msg.message_id
    await ClientStatesGroup.inviting.set()


@dp.message_handler(state=ClientStatesGroup.inviting)
async def inviting(message: types.Message, state: FSMContext):
    oponent_id = message.text
    await message.delete()
    async with state.proxy() as data:
        last_msg_id = data['last_bot_msg_id']
    await bot.edit_message_text(chat_id=message.chat.id, message_id=last_msg_id, text=f"Отправил вызов игроку {oponent_id}")
    msg = await bot.send_message(chat_id=oponent_id, text=f"Тебя вызвал: {message.chat.id}, готов принять вызов?", reply_markup=get_keyboard(message.from_user.id))
    oponent_state = dp.current_state(chat=oponent_id, user=oponent_id)
    async with oponent_state.proxy() as data:
        data['last_bot_msg_id'] = msg.message_id

@dp.callback_query_handler(lambda e: e.data.startswith("is_ready"), state=ClientStatesGroup.in_menu)
async def ready_callback(call: types.CallbackQuery, state: FSMContext):
    host_id = call.data.split('with_')[1]
    opponent_id = call.from_user.id
    player1_state = dp.current_state(chat=host_id, user=host_id)
    player2_state = dp.current_state(chat=opponent_id, user=call.from_user.id)

    async with player2_state.proxy() as data:
        opponent_last_msg_id = data['last_bot_msg_id']

    if 'not' in call.data:
        await bot.send_message(chat_id=host_id, text='Противник не готов')
        await bot.edit_message_reply_markup(chat_id=opponent_id, message_id=call.message.message_id, reply_markup=None)
    else:
        await bot.delete_message(chat_id=opponent_id, message_id=opponent_last_msg_id)
        await bot.send_message(chat_id=host_id, text='Противник принял вызов')


        match_id = json.loads(requests.get(f'http://127.0.0.1:8000/create_game/{host_id}x{opponent_id}').text)['game_id']
        async with player1_state.proxy() as data:
            data['match_id'] = match_id
            data['round'] = 1
            data['ready'] = False
            data['oponent'] = opponent_id
            data['correct_answers'] = 0

        async with player2_state.proxy() as data:
            data['match_id'] = match_id
            data['round'] = 1
            data['ready'] = False
            data['oponent'] = host_id
            data['correct_answers'] = 0

        await player1_state.set_state(ClientStatesGroup.confirmation)
        await player2_state.set_state(ClientStatesGroup.confirmation)
        host_msg = await bot.send_message(chat_id=host_id, text="Готовы начать матч?", reply_markup=go_keyboard())
        oponent_msg = await bot.send_message(chat_id=opponent_id, text="Готовы начать матч?", reply_markup=go_keyboard())
        async with player1_state.proxy() as data:
            data['last_bot_msg_id'] = host_msg.message_id
        async with player2_state.proxy() as data:
            data['last_bot_msg_id'] = oponent_msg.message_id

@dp.message_handler(state=ClientStatesGroup.confirmation)
async def wait_for_ready_both(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text == 'Начать матч':
        async with state.proxy() as data:
            match_id = data['match_id']
            round_id = data['round']
            data['ready'] = True
            oponent_id = data['oponent']
            data['cur_answer'] = None
            data['after_round_delete'] = []

        oponent_state = dp.current_state(chat=oponent_id, user=oponent_id)
        async with oponent_state.proxy() as data:
            oponent_ready = data['ready']

        if not oponent_ready:
            async with state.proxy() as data:
                last_msg_id = data['last_bot_msg_id']
            await bot.delete_message(chat_id=message.chat.id, message_id=last_msg_id)
            msg = await bot.send_message(chat_id=message.chat.id, text="Ждём, пока противник нажмёт НАЧАТЬ МАТЧ")
            async with state.proxy() as data:
                data['last_bot_msg_id'] = msg.message_id

        else:
            await state.set_state(ClientStatesGroup.round1)
            await oponent_state.set_state(ClientStatesGroup.round1)
            await asyncio.sleep(1)
            async with state.proxy() as data:
                last_msg_id = data['last_bot_msg_id']
            await bot.delete_message(chat_id=message.chat.id, message_id=last_msg_id)
            async with oponent_state.proxy() as data:
                opponent_last_msg_id = data['last_bot_msg_id']
            await bot.delete_message(chat_id=oponent_id, message_id=opponent_last_msg_id)
            await bot.send_message(chat_id=message.chat.id, text=f"Матч начинается")
            await bot.send_message(chat_id=oponent_id, text=f"Матч начинается")
            await asyncio.sleep(3)
            round_info = json.loads(requests.get(f'http://127.0.0.1:8000/game/{match_id}/get_round/{round_id}').text)
            p1_msg1_del = await bot.send_photo(chat_id=message.chat.id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
            p2_msg1_del = await bot.send_photo(chat_id=oponent_id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))

            async with state.proxy() as data:
                data['after_round_delete'].append(p1_msg1_del)

            async with oponent_state.proxy() as data:
                data['after_round_delete'].append(p2_msg1_del)

@dp.message_handler(state=(ClientStatesGroup.round1,ClientStatesGroup.round2,ClientStatesGroup.round3,ClientStatesGroup.round4,ClientStatesGroup.round5))
async def play_in_room(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        match_id = data['match_id']
        round_id = data['round']
        oponent_id = data['oponent']
        cur_answer = data['cur_answer']
        data['after_round_delete'].append(message)
    round_info = json.loads(requests.get(f'http://127.0.0.1:8000/game/{match_id}/get_round/{round_id}').text)

    if not cur_answer:
        async with state.proxy() as data:
            data['cur_answer'] = message.text
        if round_info['country'] == message.text:
            async with state.proxy() as data:
                data['correct_answers'] += 1
            msg3_del = await message.answer(text="Правильный ответ")
        else:
            msg3_del = await message.answer(text="Неправильный ответ")
        async with state.proxy() as data:
            data['after_round_delete'].append(msg3_del)
        await ClientStatesGroup.next()

        oponent_state = dp.current_state(chat=oponent_id, user=oponent_id)
        async with oponent_state.proxy() as data:
            op_cur = data['cur_answer']
            op_last_bot_msg = data['last_bot_msg_id']

        if await state.get_state() == await oponent_state.get_state() and op_cur:

            async with state.proxy() as data:
                data['cur_answer'] = None
                data['round'] += 1

            async with oponent_state.proxy() as data:
                data['cur_answer'] = None
                data['round'] += 1

            if round_id == 5:
                all_msg_del = []
                msg7_del = await bot.send_message(chat_id=message.chat.id, text=f"Противник ответил {op_cur}")
                await bot.edit_message_text(chat_id=oponent_id, message_id=op_last_bot_msg, text=f"Противник ответил {message.text}")
                async with state.proxy() as data:
                    correct_answers = data['correct_answers']
                    data['after_round_delete'].append(msg7_del)
                    all_msg_del.extend(data['after_round_delete'])
                async with oponent_state.proxy() as data:
                    op_correct_answers = data['correct_answers']
                    all_msg_del.extend(data['after_round_delete'])

                await state.set_state(ClientStatesGroup.finished_answer)
                await oponent_state.set_state(ClientStatesGroup.finished_answer)
                await bot.send_message(chat_id=message.chat.id, text=f"Вы ответили правильно на {correct_answers}/5 вопросов")
                await bot.send_message(chat_id=message.chat.id, text=f"Противник ответил правильно на {op_correct_answers}/5 вопросов", reply_markup=get_end_match_kb())
                await bot.send_message(chat_id=oponent_id, text=f"Вы ответили правильно на {op_correct_answers}/5 вопросов", reply_markup=get_end_match_kb())
                await bot.send_message(chat_id=oponent_id, text=f"Противник ответил правильно на {correct_answers}/5 вопросов",)
                await asyncio.sleep(2)
                for msg in all_msg_del:
                    await asyncio.sleep(0.1)
                    try:
                        await msg.delete()
                    except:
                        continue
            else:
                await asyncio.sleep(1)
                await bot.edit_message_text(chat_id=oponent_id, message_id=op_last_bot_msg, text=f"Противник ответил {message.text}")
                msg4_del = await bot.send_message(chat_id=message.chat.id, text=f"Противник ответил {op_cur}")
                round_info = json.loads(requests.get(f'http://127.0.0.1:8000/game/{match_id}/get_round/{round_id + 1}').text)
                await asyncio.sleep(3)
                msg5_del = await bot.send_photo(chat_id=message.chat.id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                msg7_del = await bot.send_photo(chat_id=oponent_id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                async with state.proxy() as data:
                    data['after_round_delete'].extend((msg4_del, msg5_del, msg7_del))
        else:
            msg = await bot.send_message(chat_id=message.chat.id, text="Ждём, пока противник закончит раунд")
            async with state.proxy() as data:
                data['last_bot_msg_id'] = msg.message_id
                data['after_round_delete'].append(msg)
    else:
        await message.delete()



@dp.message_handler(state=ClientStatesGroup.finished_answer)
async def finished(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Спасибо за игру!")
    await state.set_state(ClientStatesGroup.in_menu)




@dp.message_handler()
async def msg(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
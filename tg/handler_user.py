import asyncio
from datetime import datetime
from stable_diffusion import sd_gen, save_img

from aiogram import Router, Bot, F, types
import json
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject, or_f
from bot_logic import FSM, contact_user, save_input, log, load_lexicon
import keyboards
from settings import *
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
import time

# Инициализация бота
router: Router = Router()
queue: list[str] = []


# команда /start
@router.message(CommandStart())
async def start_command(message: Message, bot: Bot, state: FSMContext):
    lexicon = load_lexicon('ru')
    user = message.from_user

    # приветствие
    await message.answer(text=lexicon['start'])

    # сообщить админу, кто стартанул бота
    alert = f'➕ user {contact_user(user=user)}'
    try:
        await bot.send_message(text=alert, chat_id=admins[0], disable_notification=True, parse_mode='HTML')
    except:
        print('no admin')
        pass

    # логи
    await log(logs, user.id, f'started by {user.full_name}, @{user.username}, id {user.id}, {user.language_code}')
    await state.clear()


# команда /help
@router.message(Command(commands=['help']))
async def comm(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    lexicon = load_lexicon('ru')
    await log(logs, user, msg.text)
    await msg.answer(lexicon['help'])
    await state.clear()


# команда /generate - ввод данных для генерации
@router.message(Command(commands=['generate']))
async def personal_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    await log(logs, user, msg.text)

    # спросить pos_prompt
    language = 'ru'
    lexicon = load_lexicon(language)
    await msg.answer(lexicon['pos_prompt'], parse_mode='HTML')
    await state.set_state(FSM.pos_prompt)


# юзер отправляет промт > спросить neg_prompt
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.pos_prompt))
async def personal_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    await log(logs, user, msg.text)

    # сохранить pos_prompt
    data = {'pos_prompt': msg.text}
    save_input(users, user, data)

    # спросить neg_prompt
    language = 'ru'
    lexicon = load_lexicon(language)
    await msg.answer(lexicon['neg_prompt'], parse_mode='HTML')
    await state.set_state(FSM.neg_prompt)


# юзер отправляет neg_prompt > спросить число шагов обработки
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.neg_prompt))
async def personal_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    await log(logs, user, msg.text)

    # проверить ввод
    if msg.text.isnumeric():
        neg_prompt = None
    else:
        neg_prompt = msg.text

    # сохранить neg_prompt
    data = {'neg_prompt': neg_prompt}
    save_input(users, user, data)

    # спросить число
    language = 'ru'
    lexicon = load_lexicon(language)
    await state.set_state(FSM.steps_num)
    await msg.answer(lexicon['steps_num'], parse_mode='HTML')


# юзер отправляет число шагов > подтверждение генерации
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.steps_num))
async def personal_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    await log(logs, user, msg.text)

    language = 'ru'
    lexicon = load_lexicon(language)

    # проверка правильности ввода
    n = msg.text
    if not (n.isnumeric() and 0 < int(n) <= 30):
        # уведомить о неверном вводе
        await msg.answer(lexicon['fail_steps_num'])
        return

    # сохранить число
    data = {'steps_num': n}
    save_input(users, user, data)

    # прочитать данные юзера
    with open(users, 'r', encoding='utf-8') as f:
        data = json.load(f)
        payload: dict = data.get(user)

    # заменить ключи на норм слова
    txt_payload = ''
    trans = {
        'pos_prompt': 'Промпт',
        'neg_prompt': 'Анти-промпт',
        'steps_num': 'Число шагов',
    }
    for key, val in payload.items():
        txt_payload += f'{trans[key]}: <code>{val}</code>\n'

    print('txt_payload', txt_payload)

    # подтверждение запуска
    await msg.answer(lexicon['confirmation'].format(txt_payload),
                     reply_markup=keyboards.keyboard_confirm, parse_mode='HTML')
    await state.set_state(FSM.confirm)


# юзер нажал кнопку подтверждения генерации ✅
@router.callback_query(F.data == "ok", StateFilter(FSM.confirm))
async def confirm_gen(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user = str(callback.from_user.id)
    msg = callback.message
    await bot.edit_message_text(f'{msg.html_text}\n✅', msg.chat.id, msg.message_id, reply_markup=None, parse_mode='HTML')
    await state.clear()
    await log(logs, user, 'button_ok')
    language = 'ru'
    lexicon = load_lexicon(language)

    # очередь
    global queue
    id_in_queue = user+'_'+str(time.time())
    print(f'{id_in_queue = }')
    queue.append(id_in_queue)  # встать в очередь
    last_position = 0

    # пока в очереди есть кто-то еще другой
    while any(filter(lambda x: x != id_in_queue, queue)):
        position = queue.index(id_in_queue)+1
        # очередь кончилась
        if position == 1:
            break
        else:
            await asyncio.sleep(1)
        # очередь изменилась - уведомить
        if last_position != position:
            last_position = position
            await bot.send_message(chat_id=user, text=lexicon['queue'].format(position), disable_notification=True)

    # уведомить о запуске генерации
    await bot.send_message(chat_id=user, text=lexicon['button_ok'])

    # загрузить данные
    with open(users, 'r', encoding='utf-8') as f:
        data = json.load(f)
        payload: dict = data.get(user)

    # генерация
    start = time.time()
    img = await sd_gen(payload=payload)
    sec = int(time.time() - start)

    # сохранить
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    user_name = f"{callback.from_user.first_name}_{callback.from_user.last_name}"
    file_name = f"{user_name}_{payload.get('steps_num')}-step_{timestamp}.png"
    path = save_img(image=img, folder='users_output', file_name=file_name)
    await log(logs, user, f'gen: {path}')

    # отправить результат
    await bot.send_document(chat_id=user, document=FSInputFile(path=path), caption=lexicon['done'].format(sec))
    print(id_in_queue, 'done', sec, 'sec')
    queue.remove(id_in_queue)  # покинуть очередь
    await log(logs, user, 'success')


# юзер нажал кнопку ОТМЕНЫ генерации ❌
@router.callback_query(F.data == "no", StateFilter(FSM.confirm))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user = str(callback.from_user.id)
    msg = callback.message
    await bot.edit_message_text(f'{msg.html_text}\n❌', msg.chat.id, msg.message_id, reply_markup=None, parse_mode='HTML')

    await log(logs, user, 'button_no')
    language = 'ru'
    lexicon = load_lexicon(language)

    await bot.send_message(chat_id=user, text=lexicon['button_no'])
    await state.clear()

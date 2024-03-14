import json
from aiogram.filters import BaseFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile, User
from aiogram import Bot
from datetime import datetime
from config import config
from settings import available_languages, commands
from aiogram.types import BotCommand


# Состояния FSM, в которых будет находиться бот в разные моменты взаимодействия с юзером
class FSM(StatesGroup):
    pos_prompt = State()    # ввод данных для генерации
    neg_prompt = State()    # ввод данных для генерации
    steps_num = State()     # ввод данных для генерации
    confirm = State()       # подтверждение и запуск генерации


# Фильтр, проверяющий доступ юзера
class Access(BaseFilter):
    # фильтр принимает список со строками id
    def __init__(self, access: list[str]) -> None:
        self.access = access

    # вернуть True если юзер в списке
    async def __call__(self, message: Message) -> bool:
        user_id_str = str(message.from_user.id)
        return user_id_str in self.access


# создать команды в меню
async def set_menu_commands(bot: Bot) -> None:
    await bot.set_my_commands([BotCommand(command=item[0], description=item[1]) for item in commands.items()])
    print('Команды созданы')

    # ссылка на бота
    bot_info = await bot.get_me()
    bot_link = f"https://t.me/{bot_info.username}"
    print(bot_link)


# выбор языка. на входе языковой код (по дефолту ru), на выходе словарь с лексикой этого языка
def load_lexicon(language: str) -> dict:
    if language not in available_languages:
        language = 'ru'
    lexicon_module = __import__(f'lexic.{language}', fromlist=[''])
    return lexicon_module.lexicon


# запись логов в csv, консоль
async def log(file, key, item) -> None:
    t = str(datetime.now()).split('.')[0]
    log_text = '\t'.join((t, str(key), repr(item)))

    # сохранить в tsv
    try:
        with open(file, 'a', encoding='utf-8') as f:
            print(log_text, file=f)
    except Exception as e:
        log_text += f'\n🔴Ошибка записи в tsv:\n{e}'

    # дублировать логи в консоль
    print(log_text)


# сохранить ввод юзера в json
def save_input(file, user, payload: dict) -> None:
    # прочитать бд
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    # записать значение
    print(f'{payload = }')
    print('items', tuple(payload.items()))
    key, val = tuple(payload.items())[0]
    data.setdefault(str(user), {})[key] = val

    # сохранить бд
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# написать имя и ссылку на юзера, даже если он без username
def contact_user(user: User) -> str:
    tg_url = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'
    text = f'{tg_url} id{user.id} @{user.username}'
    return text

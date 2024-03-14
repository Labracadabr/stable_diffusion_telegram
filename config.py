from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    BOT_TOKEN: str = None           # телеграм бот
    SOME_MORE_TOKEN: str = None     # токен от еще чего-нибудь


# загрузить конфиг из переменных окружения
env = Env()
env.read_env()
config = Config(
    BOT_TOKEN=env('BOT_TOKEN_PROD'),
    # SOME_MORE_TOKEN=env(''),

)


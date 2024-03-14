# stable_diffusion_telegram

# Как запустить
1. Создать бота здесь https://t.me/BotFather и получить токен
2. Создать файл <code>.env</code> со своим токеном по примеру файла <code>example.env</code>
3. Настроить venv
4. Установить зависимости командой <code>pip install -r requirements.txt</code>
5. Запускать бота через файл <code>bot.py</code> - это точка входа

# Структура проекта
──── sd.py                  stable diffusion
──── users.json             хранение ввода пользователей
──── logs.csv               хранение логов
──── .env                   секреты
──── tg/                    папка тг-бота
──────── bot.py             точка входа
──────── bot_logic.py       функции
──────── config.py          чтение переменных окружения
──────── handler_user.py    взаимодействие с пользователем
──────── keyboards.py       кнопки
──────── settings.py        прочие настройки
──────── lexic/             языковые словари
──────────── ru.py          

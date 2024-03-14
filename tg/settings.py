import os

# список языков
available_languages = ('ru',)

# Список id админов
dima = "992863889"
admins: list[str] = [dima]

# где хранятся данные
logs = 'logs.tsv'
users = 'users.json'

# команды бота
commands = {
    "/start": "Запуск",
    "/help": "Помощь",
    "/generate": "Генерация фото"
}


# проверить все ли на месте
def check_files():
    file_list = [logs, users]
    for file in file_list:
        if not os.path.isfile(file):
            if file.endswith('json'):
                with open(file, 'w', encoding='utf-8') as f:
                    print('Отсутствующий файл создан:', file)
                    print('{}', file=f)
            elif file.endswith('sv'):
                with open(file, 'w', encoding='utf-8') as f:
                    print('Отсутствующий файл создан:', file)
                    print('\t'.join(('Time', 'User', 'Action')), file=f)


check_files()
print('OK')

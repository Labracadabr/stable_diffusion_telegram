lexicon: dict[str:str] = {
    'help': 'Нажмите /generate для ввода данных и запуска генерации фото'
    ,
    'start': 'Привет!\nЯ генерирую изображения из текста. Нажмите /generate для ввода данных и запуска генерации.',

    # данные для генерации
    'pos_prompt': 'Укажите промпт - что должно быть сгенерировано на фото. Например:\n<code>realistic red sport car in urban surrounding</code>',
    'neg_prompt': 'Укажите анти-промпт - чего не должно быть на фото. Например:\n<code>disfigured, cartoon, anime, painting, sepia, b&w</code>',
    'steps_num': 'Укажите число шагов обработки. Введите число от 1 до 50, где 1 - самый быстрый результат, 50 - самый качественный. Отправьте число от 1 до 30.\nРекомендую: <code>5</code>',
    'fail_steps_num': 'Я ожидаю число от 1 до 50',
    'confirmation': 'Ваш запрос:\n\n{}\nПриступить к генерации?',
    'button_ok': 'Генерация запущена, ожидайте',
    'button_no': 'Генерация отменена',
    'done': 'Генерация выполнена за {} секунд',

}

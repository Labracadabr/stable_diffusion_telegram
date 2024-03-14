from aiogram.types import KeyboardButton, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup, ReplyKeyboardMarkup

# кнопки
ok: Button = Button(text='✅', callback_data='ok')
no: Button = Button(text='❌', callback_data='no')

# клавиатуры из таких кнопок
keyboard_confirm = Markup(inline_keyboard=[[ok], [no]])

from aiogram.types import KeyboardButton, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup, ReplyKeyboardMarkup

# кнопки
ok: Button = Button(text='✅', callback_data='ok')
no: Button = Button(text='❌', callback_data='no')
redo: Button = Button(text='♻️', callback_data='redo')

# клавиатуры из таких кнопок
keyboard_confirm = Markup(inline_keyboard=[[ok], [no]])
keyboard_redo = Markup(inline_keyboard=[[redo]])

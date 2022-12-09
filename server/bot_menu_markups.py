from telebot import types
 
main_menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu_markup.add(types.KeyboardButton('/start'), types.KeyboardButton('/help'))

shell_menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
shell_menu_markup.add(types.KeyboardButton('Exit'))
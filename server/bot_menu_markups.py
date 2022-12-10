from telebot import types
 
main_menu_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
main_menu_markup.add(types.KeyboardButton('/init'), types.KeyboardButton('/get'), types.KeyboardButton('/help'))

shell_main_menu_markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
shell_main_menu_markup.add(types.KeyboardButton('/shell'), types.KeyboardButton('/init'), types.KeyboardButton('/help'))

shell_menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
shell_menu_markup.add(types.KeyboardButton('exit'), types.KeyboardButton('screenshot'))

init_menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
init_menu_markup.add(types.KeyboardButton('/exit'))
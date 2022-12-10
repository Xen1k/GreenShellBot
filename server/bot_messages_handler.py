from telebot import telebot
from bot_menu_markups import *
from utils import *
import os
from config import *

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), threaded=False)
bot.remove_webhook()
bot.set_webhook(url=URL + '/' + os.getenv('BOT_TOKEN'))


pending_init_codes = []
'''List of peding clients (initialization codes)'''

bot_users = {} 
'''Dict of connected bot users: 'init_code' : BotUser'''

main_menu_label = "If you have a PC client program and initialization code - run /init.\nTo get client program run /get. \n/help to show more info"
main_menu_help_label = '''For cmd commands execution Green Shell client program is needed. You can get it by typing /get.\n
After opening the program you can get initialization code by running...\n
The program starts automatically when you turn on your computer.\n
Remember, the initialization code is const and unique for each machine.'''

class BotUser:
    def __init__(self, init_code, chat_id):
        self.last_command = ''
        self.init_code = init_code
        self.chat_id = chat_id
        @bot.message_handler(content_types=['text'])
        def _get_menu_messages(message):
            self.get_menu_messages(message)

    def get_menu_messages(self, message):
        if message.text == "/shell":
            bot.send_message(message.from_user.id, "Start. Write 'exit' to terminate connection. Input shell command:", reply_markup=shell_menu_markup)
            bot.register_next_step_handler(message, self.get_shell_commands)
        elif message.text == "/init":
            bot.send_message(message.from_user.id, "Input your initialization number:", reply_markup=init_menu_markup)
            bot.register_next_step_handler(message, get_initialization_code_messages)
            del bot_users[self.init_code]
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Change working drives: 'DRIVE_NAME' + ':' (Ex: 'D:')\nEGet PC screen with 'screenshot' command\nStart with: /shell")
            bot.register_next_step_handler(message, self.get_menu_messages)
        else:
            bot.send_message(message.from_user.id, "Unknown command. Try /help or select option from keyboard below.", reply_markup=shell_main_menu_markup)
            bot.register_next_step_handler(message, self.get_menu_messages)

    def get_shell_commands(self, message):
        if(message.text.lower() == 'exit'): 
            bot.send_message(message.from_user.id, 'Terminated', reply_markup=shell_main_menu_markup)
            bot.register_next_step_handler(message, self.get_menu_messages)
            self.last_command = ''
            return
        self.last_command = message.text


def get_initialization_code_messages(message):
        if message.text.lower() == '/exit':
            bot.send_message(message.from_user.id, main_menu_label, reply_markup=main_menu_markup)
            bot.register_next_step_handler(message, get_main_menu_messages)  
        elif message.text in pending_init_codes:
            # Initialize new user
            new_user = BotUser(init_code=message.text, chat_id=message.from_user.id)
            bot_users[message.text] = new_user
            bot.send_message(message.from_user.id, 
                            "Initialized.\nRun /shell to connect to pc.\nInitialize again with /init. \n/help for info",
                            reply_markup=shell_main_menu_markup)
            bot.register_next_step_handler(message, new_user.get_menu_messages)  
            # Remove from pending 
            pending_init_codes.remove(message.text)
        else:
            if message.text in bot_users:
                bot.send_message(message.from_user.id, "This client has already been initialized. Try again. (Or /exit to exit to main menu)")
            else:
                bot.send_message(message.from_user.id, "Wrong initialization code. Try again. (Or /exit to exit to main menu)")
            bot.register_next_step_handler(message, get_initialization_code_messages)

@bot.message_handler(content_types=['text'])
def handle_first_message(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, main_menu_label, reply_markup=main_menu_markup)
        bot.register_next_step_handler(message, get_main_menu_messages)
    else:
        bot.send_message(message.from_user.id, "Try /start")

def get_main_menu_messages(message):
    if message.text == "/init":
        bot.send_message(message.from_user.id, "Input your initialization number (Or /exit to exit to main menu):", reply_markup=init_menu_markup)
        bot.register_next_step_handler(message, get_initialization_code_messages)
    else:
        if message.text == "/get":
            bot.send_message(message.from_user.id, "Download program here: ...")
        elif message.text == "/help":
            bot.send_message(message.from_user.id, main_menu_help_label)
        else:
            bot.send_message(message.from_user.id, "Try /help")
        bot.register_next_step_handler(message, get_main_menu_messages)





  



   


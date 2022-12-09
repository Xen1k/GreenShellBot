from telebot import telebot
from bot_menu_markups import *
from utils import *
import os
from config import *

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), threaded=False)
bot.remove_webhook()
bot.set_webhook(url=URL + '/' + os.getenv('BOT_TOKEN'))


bot_users = {} # "'client-id' : object"

class UserInitilizer:
    """Handles user initializtion process."""
    def __init__(self):
        self.last_client_id = '' 
        """ last typed initialization code (including messages from all users)"""

        self.last_telegram_user_id = '' 
        """last typed telegram user id (including messages from all users)"""

        self.last_message = None
        """last typed message (including messages from all users)"""

    def get_initialization_code_messages(self, message):
        self.last_client_id = message.text
        self.last_telegram_user_id = message.from_user.id
        self.last_message = message

user_initializer = UserInitilizer()


class BotMessagesHandler:
    def __init__(self, client_id):
        self.last_command = ''
        self.last_command_reply = ''
        self.telegram_user_id = '' # Necessarry?
        self.client_id = client_id # Necessarry?
        @bot.message_handler(content_types=['text'])
        def _get_menu_messages(message):
            self.get_menu_messages(message)
      

    def get_menu_messages(self, message):
        if message.text == "/shell":
            bot.send_message(message.from_user.id, "Start. Write 'exit' to terminate connection. Input shell command:", reply_markup=shell_menu_markup)
            bot.register_next_step_handler(message, self.__get_shell_commands)
        if message.text == "/init":
            bot.send_message(message.from_user.id, "Input your initialization number:")
            bot.register_next_step_handler(message, user_initializer.get_initialization_code_messages)
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Change working drives: 'DRIVE_NAME' + ':' (Ex: 'D:')\nStart with: /shell")
        else:
            bot.send_message(message.from_user.id, "Unknown command. Try /help or select option from keyboard below.", reply_markup=main_menu_markup)



    def __get_shell_commands(self, message):
        if(message.text.lower() == 'exit'): 
            bot.send_message(message.from_user.id, 'Terminated', reply_markup=main_menu_markup)
            return
        self.last_command = message.text
        wait_until(lambda: len(self.last_command_reply) > 0)
        bot.send_message(message.from_user.id, self.last_command_reply)
        self.last_command_reply = ''
        bot.register_next_step_handler(message, self.__get_shell_commands)


  



   


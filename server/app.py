from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from flask_socketio import SocketIO, emit
from telebot import telebot
from bot_messages_handler import *
from config import *
from utils import *
import os


app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('initialize_new_client')
def initialize_new_client(new_client_id):
    wait_until(lambda: user_initializer.last_client_id == new_client_id)
    emit('set_initialized', new_client_id)
    bot.send_message(user_initializer.last_telegram_user_id, "Initialized")
    new_user = BotMessagesHandler(new_client_id)
    bot_users[new_client_id] = new_user
    bot.register_next_step_handler(user_initializer.last_message, new_user.get_menu_messages)

@socketio.on('command_response')
def handle_command_response(data):
    client_id = data.split()[0] # data = client_id + ' ' + command_reply
    try:
        current_user = bot_users.get(client_id) 
    except:
        print("Fatal. No such user.")
        return
    try:
        current_user.last_command_reply = data[(len(client_id) + 1)::]
    except:
        current_user.last_command_reply = ''
    wait_until(lambda: len(current_user.last_command) > 0)
    emit('handle_bot_command', current_user.last_command)
    current_user.last_command = ''

@app.route('/{}'.format(os.getenv('BOT_TOKEN')), methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Connected", 200

@bot.message_handler(commands=['start'])
def get_start_menu_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Input your initialization number:")
        bot.register_next_step_handler(message, user_initializer.get_initialization_code_messages)
        
    else:
        bot.send_message(message.from_user.id, "Try /start")


if __name__ == '__main__':
    socketio.run(app, port=os.environ.get('PORT', 80), use_reloader=True)

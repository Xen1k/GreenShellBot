import time
import base64

def wait_until(delegate):
    while not delegate():
        time.sleep(0.05)

def convert_string_to_binary_image(binary_string):
    ''' Converts string image (after encoding binary) to decoded binary '''
    return base64.b64decode(binary_string.encode(encoding='UTF-8'))
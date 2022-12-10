from PIL import ImageGrab
import base64
import os

def get_screenshot_as_string(destination, mime='JPEG'):
    _screenshot = ImageGrab.grab()
    _screenshot.save(destination, mime)
    with open(destination, "rb") as screenshot:
        converted_string = base64.b64encode(screenshot.read())
    os.remove(destination)
    return converted_string.decode(encoding='UTF-8')
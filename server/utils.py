import time

def wait_until(delegate):
    while not delegate():
        time.sleep(0.05)
    
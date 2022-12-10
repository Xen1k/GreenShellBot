from uuid import getnode

def generate_init_code(): 
    init_code = getnode()
    while len(str(int(init_code))) > 5:
        init_code /= 2.
    return int(init_code)
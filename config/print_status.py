import time


def print_status(status):
    # Imprime el estado y regresa al inicio de la línea
    print("                                                        ", end='\r')
    print(status, end='\r')


def clear_status():
    print("                                                        ", end='\r')


spinner_values = ['|', '/', '-', '\\']
spinner_index = 0
last_second = 0

def print_spinner():
    global last_second
    current_second = int(time.time())

    if current_second != last_second:
        print_status(spinner_values[next_spinner_index()])
        last_second = current_second

def next_spinner_index():
    global spinner_index
    if spinner_index == 3:
        spinner_index = 0
    else:
        spinner_index = spinner_index + 1
    return spinner_index
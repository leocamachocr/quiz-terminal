

def print_banner():
    print()
    with open('resources/banner.txt', 'r') as file:
        content = file.read()
    print(content)

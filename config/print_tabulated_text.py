def print_tabulated_text(text, width):
    lines = text.split('\n')
    for line in lines:
        print("{:<{}}".format(line, width))


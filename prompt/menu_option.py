class MenuOption:
    def __init__(self, id, text, command):
        self.id = id
        self.text = text
        self.command = command


def invoke_option(menu_options, option_id):
    for option in menu_options:
        if option.id == option_id:
            option.command.execute()
            return
    print("Invalid option.")

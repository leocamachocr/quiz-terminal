from commands.command import Command, Invoker
from commands.settings.add_author import AddAuthor
from commands.settings.add_custom_filter import CreateCustomFilter


class SettingsMenu(Command):
    def execute(self):
        print("Settings Menu")
        print("1. Add an author")
        print("2. Create custom filter")
        print("3. Back to main menu")

        option = input("Seleccione una opción: ")

        if option == "1":
            add_author = AddAuthor()
            invoker = Invoker(add_author)
            invoker.invoke()
        elif option == "2":
            custom_filter = CreateCustomFilter()
            invoker = Invoker(custom_filter)
            invoker.invoke()
        elif option == "3":
            print("Returning to main menu...")
        else:
            print("Invalid option.")

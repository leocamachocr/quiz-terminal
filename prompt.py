from commands.consolidate_files import ConsolidateFiles
from commands.load_questions import LoadQuestions
from commands.quiz_command import QuizCommand
from commands.remove_and_copy_files import RenameAndCopyFiles
from config.init_config import Config
from config.print_banner import print_banner
from prompt.menu_option import MenuOption, invoke_option

print_banner()
Config()
menu_options = [
    # MenuOption("1", "List all repositories", ListAllRepos()),
    MenuOption("10", "Consolidate files from directory", ConsolidateFiles()),
    MenuOption("11", "Remove and Copy", RenameAndCopyFiles()),
    MenuOption("12", "Quiz", QuizCommand()),
    MenuOption("X", "Exit", None)
]
for option in menu_options:
    print(f"{option.id}. {option.text}")

option_id = input("Seleccione una opción: ")
invoke_option(menu_options, option_id)

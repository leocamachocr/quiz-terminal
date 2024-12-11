import os
from config.init_config import Config

class FilterFilesCommand:
    def __init__(self):
        self.config = Config()
        self.questions_path = self.config.get_questions_path()

    def execute(self):
        # Step 1: Read all files in the directory
        files = os.listdir(self.questions_path)

        # Step 2: Separate file names by '-'
        separated_names = [file.split('-') for file in files]

        # Step 3: Show all different values from node 0 of the names
        node_0_values = set(name[0] for name in separated_names)
        print("Different values from node 0 of the names:")
        for value in node_0_values:
            print(value)

        # Step 4: Ask for a prefix to use
        prefix = input("Enter the prefix you want to use: ")

        # Step 5: Show files that match the prefix
        matching_files = [file for file in files if file.startswith(prefix)]
        print("Files that match the prefix:")
        for file in matching_files:
            print(file)

        # Step 6: Ask for files containing a certain word
        word = input("Enter the word to filter files: ")
        filtered_files = [file for file in matching_files if word in file]
        print("Files that contain the word:")
        for file in filtered_files:
            print(file)

        # Step 7: Return a list with the paths of the selected files and the prefix
        selected_files = [os.path.join(self.questions_path, file) for file in filtered_files]
        return selected_files, prefix

if __name__ == "__main__":
    command = FilterFilesCommand()
    selected_files, prefix = command.execute()
    print("Selected files:")
    for file in selected_files:
        print(file)
    print("Selected prefix:", prefix)
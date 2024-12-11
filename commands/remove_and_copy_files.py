import os
import shutil

class RenameAndCopyFiles:
    def execute(self):
        input_dir = input("Enter the input directory: ")
        output_dir = input("Enter the output directory: ")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for root, dirs, files in os.walk(input_dir):
            for dir_name in dirs:
                # Process the directory name
                name_parts = dir_name.split('_')[0].split()
                if len(name_parts) < 2:
                    continue
                new_name = ' '.join(name_parts[-2:] + name_parts[:-2])

                # Get the first file in the directory
                dir_path = os.path.join(root, dir_name)
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)
                    if os.path.isfile(file_path):
                        # Get the file extension
                        _, extension = os.path.splitext(file_name)
                        # Create the new file name
                        new_file_name = new_name + extension
                        new_file_path = os.path.join(output_dir, new_file_name)
                        # Copy the file to the output directory with the new name
                        shutil.copy(file_path, new_file_path)
                        break

if __name__ == "__main__":
    command = RenameAndCopyFiles()
    command.execute()
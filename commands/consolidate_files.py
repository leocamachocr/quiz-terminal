import os
import logging
from commands.command import Command

class ConsolidateFiles(Command):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def execute(self):
        directory = input("Please enter the directory path: ")
        output_file = input("Please enter the name of the final output file: ")
        prefix = input("Please enter the prefix to identify the files: ")
        logging.debug(f"Directory entered: {directory}")
        logging.debug(f"Output file name entered: {output_file}")
        logging.debug(f"Prefix entered: {prefix}")
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(directory):
                logging.debug(f"Current directory: {root}")
                # Filter out directories that start with a dot
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                logging.debug(f"Filtered directories: {dirs}")
                for file in sorted(files):
                    if file.startswith(prefix):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, directory)
                        logging.debug(f"Processing file: {file_path}")
                        outfile.write(f"File: {relative_path}\n")
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read())
                        except UnicodeDecodeError as e:
                            logging.error(f"Error reading file {file_path}: {e}")
                        outfile.write("\n\n")
        logging.info(f"All files with prefix '{prefix}' have been consolidated into {output_file}")
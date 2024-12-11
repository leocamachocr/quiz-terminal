import json
import os

from commands.command import Command


class AddAuthor(Command):
    def execute(self):
        # Ask the user for the GitHub username and author alias
        username = input("Enter the GitHub username: ")
        alias = input("Enter the author alias: ")

        # Create a dictionary for the new author
        new_author = {
            'username': username,
            'alias': alias
        }

        # Check if the file exists
        if not os.path.exists('resources/authors.json'):
            # If not, create it and write the new author data
            with open('resources/authors.json', 'w') as f:
                json.dump([new_author], f)
        else:
            # If it exists, read the existing data
            with open('resources/authors.json', 'r', encoding='utf-8') as f:
                authors = json.load(f)
            # Add the new author data
            authors.append(new_author)
            # Write the updated data back to the file
            with open('resources/authors.json', 'w') as f:
                json.dump(authors, f)

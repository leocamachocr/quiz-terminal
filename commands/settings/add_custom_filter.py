import json
import os

from commands.command import Command


class CreateCustomFilter(Command):
    def execute(self):
        # Solicitar al usuario que ingrese los datos
        filter_name = input("Enter filter name: ")
        repos = input("Enter repo names(comma separated): ").split(',')
        aliases = input("Enter aliases name(comma separated): ").split(',')

        # Crear un diccionario con los datos ingresados
        new_filter = {
            "filter_name": filter_name,
            "repos": repos,
            "aliases": aliases
        }

        file_path = os.path.join('resources', 'custom_filters.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                filters = json.load(f)
            filters.append(new_filter)
        else:
            filters = [new_filter]

        with open(file_path, 'w') as f:
            json.dump(filters, f, indent=4)

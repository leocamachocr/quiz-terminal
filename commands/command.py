from abc import ABC, abstractmethod


# Clase abstracta Command
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# Clase Invoker
class Invoker:
    def __init__(self, command):
        self.command = command

    def invoke(self):
        self.command.execute()

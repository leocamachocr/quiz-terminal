# Clase LoadQuestions en el archivo commands/load_questions.py
import json
from commands.command import Command
from models.question import Question

class LoadQuestions(Command):
    def __init__(self, file_path):
        self.file_path = file_path
        self.questions = []

    def execute(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                question = Question(
                    question=item['question'],
                    options=item['options'],
                    answers_index=item['answersIndex'],
                    tags=item['tags'],
                    explanation=item['explanation']
                )
                self.questions.append(question)
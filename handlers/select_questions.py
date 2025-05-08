import os
import json
import random
from datetime import datetime

def select_questions(question_dir,prefix, questions, num_questions):
    # Construir la ruta del archivo de respuestas
    answers_file = os.path.join(self.questions_dir, f"{prefix}-answers.json")
    answered_ids = set()

    # Leer el archivo de respuestas si existe
    if os.path.exists(answers_file):
        with open(answers_file, 'r', encoding='utf-8') as file:
            answers_data = json.load(file)
            answered_ids = {answer['id'] for answer in answers_data}

    # Separar preguntas no respondidas y respondidas
    unanswered_questions = [q for q in questions if q.id not in answered_ids]
    answered_questions = [q for q in questions if q.id in answered_ids]

    # Seleccionar preguntas aleatorias
    selected_questions = random.sample(unanswered_questions, min(len(unanswered_questions), num_questions))

    # Completar con preguntas respondidas si es necesario
    if len(selected_questions) < num_questions:
        remaining_count = num_questions - len(selected_questions)
        selected_questions += random.sample(answered_questions, min(len(answered_questions), remaining_count))

    return selected_questions
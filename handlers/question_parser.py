import json
from models.question import Question

class QuestionParser:
    def __init__(self, json_input):
        self.json_input = json_input

    def parse_questions(self):
        question_dicts = json.loads(self.json_input)
        questions = []
        for q in question_dicts:
            q['answers_index'] = q.pop('answersIndex')
            questions.append(Question(**q))
        return questions
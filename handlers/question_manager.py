import json
from datetime import datetime

class QuestionManager:
    def __init__(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as file:
            self.questions = json.load(file)
        self.config_file = config_file

    def update_answer(self, question_id, is_correct):
        for question in self.questions:
            if question['id'] == question_id:
                question['answers'].append(is_correct)
                question['lastAnswer'] = datetime.now().isoformat()
                break
        self._save_config()

    def _save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(self.questions, file, indent=2, ensure_ascii=False)


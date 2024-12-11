# Clase Question
class Question:
    def __init__(self,id, question, options, answers_index, tags, explanation):
        self.id = id
        self.question = question
        self.options = options
        self.answersIndex = answers_index
        self.tags = tags
        self.explanation = explanation
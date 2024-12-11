import json
import os
import random
from datetime import datetime
from handlers.file_content_fetcher import FileContentFetcher
from handlers.question_parser import QuestionParser
from config.init_config import Config
from commands.filter_file_command import FilterFilesCommand

class QuizCommand:
    def __init__(self):
        self.answers_file = None
        self.questions_dir = Config().get_questions_path()
        self.questions = []


    def load_questions(self, files):
        for file in files:
            fetcher = FileContentFetcher(os.path.dirname(file), os.path.basename(file))
            file_contents = fetcher.fetch_contents()
            for content in file_contents:
                parser = QuestionParser(content)
                questions = parser.parse_questions()
                self.questions.extend(questions)

    def load_answers(self):
        if os.path.exists(self.answers_file):
            with open(self.answers_file, 'r', encoding='utf-8') as file:
                self.answers = json.load(file)
        else:
            self.answers = []

    def save_answer(self, question_id, is_correct):
        for answer in self.answers:
            if answer['id'] == question_id:
                answer['answers'].append(is_correct)
                answer['lastAnswer'] = datetime.now().isoformat()
                break
        else:
            self.answers.append({
                'id': question_id,
                'answers': [is_correct],
                'lastAnswer': datetime.now().isoformat()
            })
        with open(self.answers_file, 'w', encoding='utf-8') as file:
            json.dump(self.answers, file, indent=2, ensure_ascii=False)

    def save_incorrect_answers(self, incorrect_questions):
        config = Config()
        questions_path = config.get_responses_path()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        incorrect_file_path = os.path.join(questions_path, f"answers-{timestamp}.txt")

        # Ensure the directory exists
        os.makedirs(os.path.dirname(incorrect_file_path), exist_ok=True)

        with open(incorrect_file_path, 'w', encoding='utf-8') as file:
            for question in incorrect_questions:
                file.write(f"ID: {question.id}\n")
                file.write(question.question + "\n")
                for i, option in enumerate(question.options):
                    file.write(f"{i + 1}. {option}\n")
                file.write("Explanation: " + question.explanation + "\n")
                file.write("\n---\n")

        print(f"\nIncorrect questions have been saved to {incorrect_file_path}")

    def execute(self):
        # Execute the FilterFilesCommand to get the filtered files
        filter_command = FilterFilesCommand()
        filtered_files,prefix = filter_command.execute()
        self.answers_file = os.path.join(self.questions_dir, f"{prefix}-answers.json")
        self.load_answers()
        # Load questions from the filtered files
        self.load_questions(filtered_files)

        num_questions = int(input("Enter the number of questions: "))
        selected_questions = random.sample(self.questions, num_questions)

        correct_answers = 0
        incorrect_questions = []

        for question in selected_questions:
            # Get the number of answers for the question
            num_answers = len(question.answersIndex)
            print(f"\n{question.question} ({num_answers} answers)")
            for i, option in enumerate(question.options):
                print(f"{i + 1}. {option}")

            user_answer = input("Enter your answer (for multiple answers, separate by commas, or type 'wq' to save and quit, 'q' to quit): ")
            if user_answer.lower() == 'wq':
                self.save_incorrect_answers(incorrect_questions)
                print("Quiz ended and incorrect answers saved.")
                return
            elif user_answer.lower() == 'q':
                print("Quiz ended without saving.")
                return

            user_answer_indices = [int(x) - 1 for x in user_answer.split(',')]

            if set(user_answer_indices) == set(question.answersIndex):
                correct_answers += 1
                print("\033[92mCorrect!\033[0m")  # Green text
                self.save_answer(question.id, True)
            else:
                incorrect_questions.append(question)
                correct_options = ", ".join([question.options[i] for i in question.answersIndex])
                print(f"\033[92mCorrect answer: {correct_options}\033[0m")  # Green text
                print("\033[90mExplanation: " + question.explanation + "\033[0m")  # Dark gray text
                self.save_answer(question.id, False)

        print("\nQuiz Summary:")
        print(f"Correct answers: {correct_answers}")
        print(f"Incorrect answers: {len(incorrect_questions)}")

        if incorrect_questions:
            self.save_incorrect_answers(incorrect_questions)

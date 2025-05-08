import json
import os
import random
from datetime import datetime
from handlers.file_content_fetcher import FileContentFetcher
from handlers.question_parser import QuestionParser
from config.init_config import Config
from commands.filter_file_command import FilterFilesCommand


class CLIStyle:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    SEPARATOR = '-' * 60

    @staticmethod
    def success(msg): print(f"{CLIStyle.GREEN}{msg}{CLIStyle.RESET}")
    @staticmethod
    def error(msg): print(f"{CLIStyle.RED}{msg}{CLIStyle.RESET}")
    @staticmethod
    def info(msg): print(f"{CLIStyle.CYAN}{msg}{CLIStyle.RESET}")
    @staticmethod
    def headline(msg): print(f"{CLIStyle.BOLD}{msg}{CLIStyle.RESET}")


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
        os.makedirs(os.path.dirname(incorrect_file_path), exist_ok=True)

        with open(incorrect_file_path, 'w', encoding='utf-8') as file:
            for question in incorrect_questions:
                file.write(f"ID: {question.id}\n")
                file.write(question.question + "\n")
                for i, option in enumerate(question.options):
                    file.write(f"{i + 1}. {option}\n")
                file.write("Explanation: " + question.explanation + "\n")
                file.write("\n---\n")

        CLIStyle.info(f"\nIncorrect questions have been saved to {incorrect_file_path}")

    def execute(self):
        CLIStyle.headline("\n===== QUIZ CLI =====")

        filter_command = FilterFilesCommand()
        filtered_files, prefix = filter_command.execute()
        self.answers_file = os.path.join(self.questions_dir, f"{prefix}-answers.json")
        self.load_answers()
        self.load_questions(filtered_files)

        CLIStyle.info(f"\n{len(self.questions)} questions loaded from {len(filtered_files)} files.")
        print(CLIStyle.SEPARATOR)

        while True:
            try:
                num_questions = int(input("Enter the number of questions: "))
                if num_questions < 1 or num_questions > len(self.questions):
                    raise ValueError
                break
            except ValueError:
                CLIStyle.error("⚠ Please enter a valid number within the range.")

        selected_questions = random.sample(self.questions, num_questions)
        correct_answers = 0
        incorrect_questions = []

        for idx, question in enumerate(selected_questions, 1):
            num_answers = len(question.answersIndex)

            CLIStyle.headline(f"\nQuestion {idx}:")
            print(f"{question.question} ({num_answers} correct answer{'s' if num_answers > 1 else ''})\n")
            for i, option in enumerate(question.options):
                print(f"  {i + 1}. {option}")
            print(CLIStyle.SEPARATOR)

            user_answer = input("Your answer (comma-separated, 'wq' to save & quit, 'q' to quit): ").strip()

            if user_answer.lower() == 'wq':
                self.save_incorrect_answers(incorrect_questions)
                CLIStyle.info("Quiz ended and incorrect answers saved.")
                return
            elif user_answer.lower() == 'q':
                CLIStyle.info("Quiz ended without saving.")
                return

            try:
                user_answer_indices = [int(x.strip()) - 1 for x in user_answer.split(',')]
                if not all(0 <= idx < len(question.options) for idx in user_answer_indices):
                    raise ValueError
            except ValueError:
                CLIStyle.error("⚠ Invalid input. Please enter valid numbers.")
                continue

            if set(user_answer_indices) == set(question.answersIndex):
                correct_answers += 1
                CLIStyle.success("✅ Correct!")
                self.save_answer(question.id, True)
            else:
                incorrect_questions.append(question)
                correct_options = ", ".join([question.options[i] for i in question.answersIndex])
                CLIStyle.error("❌ Incorrect.")
                CLIStyle.success(f"✔ Correct answer: {correct_options}")
                CLIStyle.info(f"📘 Explanation: {question.explanation}")
                self.save_answer(question.id, False)

        CLIStyle.headline("\n===== QUIZ SUMMARY =====")
        print(f"✅ Correct answers: {correct_answers}")
        print(f"❌ Incorrect answers: {len(incorrect_questions)}")
        print(CLIStyle.SEPARATOR)

        if incorrect_questions:
            self.save_incorrect_answers(incorrect_questions)

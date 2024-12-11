import os

class FileContentFetcher:
    def __init__(self, directory_path, prefix):
        self.directory_path = directory_path
        self.prefix = prefix

    def fetch_contents(self):
        contents = []
        for filename in os.listdir(self.directory_path):
            if filename.startswith(self.prefix):
                with open(os.path.join(self.directory_path, filename), 'r', encoding='utf-8') as file:
                    contents.append(file.read())
        return contents
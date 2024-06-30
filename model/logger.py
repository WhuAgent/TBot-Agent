import json
import os

from datetime import datetime


class Logger:
    def __init__(self, root, prefix=""):
        if not os.path.exists(root):
            os.makedirs(root)
        self.root = root

        start_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.file_name = f"{prefix}-{start_time}.txt" if prefix else f"{start_time}.txt"
        self.file_path = os.path.join(self.root, self.file_name)

    def log(self, content):
        if not isinstance(content, str):
            content = json.dumps(content, indent=4)
        with open(self.file_path, 'a', encoding="UTF-8") as f:
            f.write(content)
            f.write("\n")
            f.write("\n")

    def rename(self, success):
        file_name, extension = self.file_name.split(".")
        success = 'success' if success else 'fail'
        new_file_name = f"{file_name}-{success}.{extension}"
        new_file_path = os.path.join(self.root, new_file_name)
        os.rename(self.file_path, new_file_path)
        self.file_name = new_file_name
        self.file_path = new_file_path


import os


class Logger:
    def __init__(self, root):
        if not os.path.exists(root):
            os.makedirs(root)
        self.root = root

        self.file_name = f"all.log"
        self.file_path = os.path.join(self.root, self.file_name)

        with open(self.file_path, "w", encoding="UTF-8") as f:
            f.write("")

    def log(self, cur_time, role="", content="", class_name="", output=True):
        buffer = f"[{cur_time}]"
        if class_name:
            buffer += f"[{class_name}]"
        if role:
            buffer += f"[{role}]"
        buffer += f"\n{content}\n\n"

        if output:
            print(buffer)
        with open(self.file_path, 'a', encoding="UTF-8") as f:
            f.write(buffer)

    def rename(self, success):
        file_name, extension = self.file_name.split(".")
        success = 'success' if success else 'fail'
        new_file_name = f"{file_name}-{success}.{extension}"
        new_file_path = os.path.join(self.root, new_file_name)
        os.rename(self.file_path, new_file_path)
        self.file_name = new_file_name
        self.file_path = new_file_path


import yaml
import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from utils.llm import chat_llm


class Extractor(Extension):
    def extendMarkdown(self, md):
        # 向 Markdown 实例添加一个自定义的树处理器
        md.treeprocessors.register(ExtractorProcessor(), 'extractor', 15)


class ExtractorProcessor(Treeprocessor):
    def __init__(self):
        super(ExtractorProcessor, self).__init__()
        self.demand = ""
        self.commands = []

    def run(self, root):
        for elem in root.iter():
            if elem.tag == 'p':
                self.demand = elem.text
            elif elem.tag == 'li':
                self.commands.append(elem.text)


def get_task_and_commands(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # 创建 Markdown 实例并添加自定义的提取器
    md = markdown.Markdown(extensions=[Extractor()])

    # 转换 Markdown 为 HTML
    _ = md.convert(markdown_text)

    extractor = md.treeprocessors["extractor"]

    return {
        "task": extractor.demand,
        "commands": extractor.commands
    }

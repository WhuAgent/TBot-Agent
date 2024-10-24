import yaml
import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from bs4 import BeautifulSoup

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


def get_task_and_plan(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # 创建 Markdown 实例并添加自定义的提取器
    md = markdown.Markdown()

    # 转换 Markdown 为 HTML
    md_html = md.convert(markdown_text)

    soup = BeautifulSoup(md_html, 'html.parser')

    task = soup.find("p").get_text()
    plan = soup.find_all("li")
    plan = [item.get_text() for item in plan]

    return {
        "task": task,
        "plan": plan
    }

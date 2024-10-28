import yaml

from tbot.utils.logger import Logger
from agent_network.network.graph import Graph, GraphStart
from agent_network.pipeline.pipeline import Pipeline

logger = Logger("tbot/log")

config_path = "tbot/config/agent_net/pipline.yaml"

with open(config_path, "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)


def run_task(task):
    pipeline = Pipeline(task, config, logger)
    graph = Graph('graph', None, None, None)
    graph_start = GraphStart(graph)
    pipeline.execute(graph_start)


if __name__ == "__main__":
    # run_task(
    #     '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx" 和文档 "C:/Users/lornd/Desktop/TBot/res.docx"，'
    #     '并将 origin.docx 中的所有内容复制到 res.docx 中')
    
    # run_task("请帮我把 C:/Users/lornd/Desktop/TBot/origin.docx 中的内容复制一份到 C:/Users/lornd/Desktop/TBot/res.docx")
    # # WordOpenDocument
    # run_task("请帮我打开 C:/Users/1/Downloads/123.docx 文件")
    # # WordSaveDocument
    # run_task("请帮我打开 C:/Users/1/Downloads/123.docx 文件，输入234，并保存")
    # WordSaveAsDocument
    run_task("请帮我打开 C:/Users/1/Downloads/123.docx 文件，并另存为234.docx")

import multiprocessing

from tbot.utils.logger import Logger
from agent_network.pipeline.pipeline import  Pipeline

logger = Logger("tbot/log")

config_path = "tbot/config/pipline.yaml"

def run_task(task, context):
    pipeline = Pipeline(config_path, logger, context)
    pipeline.forward(task)

if __name__ == "__main__":
    # multiprocessing_manager = multiprocessing.Manager()
    #
    # context = multiprocessing_manager.dict()

    context = dict()

    run_task(
        '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx" 和文档 "C:/Users/lornd/Desktop/TBot/res.docx"，'
        '并将 origin.docx 中的所有内容复制到 res.docx 中', context)

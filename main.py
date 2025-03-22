import json

from agent_network.graph.graph import Graph
from agent_network.constant import network, logger

def run_task(context):
    assert context['flowId'] is not None, "智能体流程节点未找到"
    assert context['task'] is not None, "智能体任务未找到"
    
    graph = Graph(logger)
    graph.execute(network, context['flowId'], context['params'], context["results"])
    result = graph.retrieve_results(context["results"])
    graph.release()
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    file_path = "data/xml/2bb16c35-403a-4d4c-859e-a88ccd55f876.xml"
    
    # 原始英文问题
    # In this academic paper, in a bar of chocolate that had the percentage makeup of the literature data's milk chocolate, what were the percentages of non-fiber carbohydrates measured along with the percentage of protein and percentage of fat to find the non-fiber carbohydrate content if they had a 2:1 ratio in the order they appeared in the paper, given in that same order in the answer as X, Y (without % sign)?
    
    # 翻译成中文的问题
    task = "在这篇学术论文中，有一块巧克力的成分百分比与文献数据中的牛奶巧克力相符。请问测量的非纤维碳水化合物百分比是多少？同时，蛋白质百分比和脂肪百分比按照它们在论文中出现的顺序是2:1的比例。请按照同样的顺序（不带%符号）给出答案，形式为X，Y。"
    
    context = {
        "flowId": "worker",
        "task": task,
        "params": {
            "task": task,
            "file_path": file_path,
        },
        "results": {
            "result": "学术论文分析结果"
        }
    }
    
    run_task(context)

    # task = '请帮我打开文档 "C:/Users/1206232012/Desktop/test.docx" ，插入一张图片，图片位置为 "C:/Users/1206232012/Desktop/家乡.jpg" 。不需要保存和关闭文档。'
    # task = '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx"。'

    # task = '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx" 和文档 "C:/Users/lornd/Desktop/TBot/res.docx"，\
    #         并将 origin.docx 中的所有内容复制到 res.docx 中'
    # task ='请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx"，\
    # 打开文档后，将光标向下移动两行并选中途径文本，\
    # 查找"测试" 并选中，\
    # 选中第二行到第三行，\
    # 删除选中文本'
    
    # task = '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx"。'

    # task = '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx" 和文档 "C:/Users/lornd/Desktop/TBot/res.docx"，\
    #         并将 origin.docx 中的所有内容复制到 res.docx 中'
    
    # task = "请帮我把 C:/Users/lornd/Desktop/TBot/origin.docx 中的内容复制一份到 C:/Users/lornd/Desktop/TBot/res.docx"

    # task = '请帮把文档 "C:/Users/lornd/Desktop/TBot/1.docx" 和文档 "C:/Users/lornd/Desktop/TBot/2.docx" 中的内容 \
    #         分别通过剪切和复制的方式粘贴到第三个文档 "C:/Users/lornd/Desktop/TBot/res.docx" 中。\
    #         在进行剪切、复制等操作前，请注意要先打开文档。'
    #
    
    # run_task("请帮我把 C:/Users/lornd/Desktop/TBot/origin.docx 中的内容复制一份到 C:/Users/lornd/Desktop/TBot/res.docx")

    # WordOpenDocument
    # run_task("请帮我打开 C:/Users/1/Downloads/123.docx 文件")
    # # WordSaveDocument
    # run_task("请帮我打开 C:/Users/1/Downloads/123.docx 文件，输入234，并保存")
    # WordSaveAsDocument
    # run_task("请帮我打开 C:/Users/1/Downloads/123.docx 文件，并另存为234.docx")

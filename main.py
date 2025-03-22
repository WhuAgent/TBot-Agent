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
    file_path = "D:\\Awork\\2025spring\\TBot-Agent\\test_data\\bird.jpg"# "C:\\Users\\lornd\\Downloads\\FC804E96CF497636909FC43BE21_07186CAC_E21D4.jpg"
    task = f"图片中的动物是什么动物 {file_path}"
    
    context = {
        "flowId": "worker",
        "task": task,
        "params": {
            "task": task,
            "file_path": file_path,
        },
        "results": {
            "result": "猫的数量"
        }
    }
    
    run_task(context)

    # task = '请帮我打开文档 "C:/Users/1206232012/Desktop/test.docx" ，插入一张图片，图片位置为 "C:/Users/1206232012/Desktop/家乡.jpg" 。不需要保存和关闭文档。'
    # task = '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx"。'

    # task = '请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx" 和文档 "C:/Users/lornd/Desktop/TBot/res.docx"，\
    #         并将 origin.docx 中的所有内容复制到 res.docx 中'
    # task ='请帮我打开文档 "C:/Users/lornd/Desktop/TBot/origin.docx"，\
    # 打开文档后，将光标向下移动两行并选中途径文本，\
    # 查找“测试” 并选中，\
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

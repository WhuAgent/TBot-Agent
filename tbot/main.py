from tbot.agent import TBotAgent


def run_task(task):
    agent = TBotAgent(task)
    plan = agent.plan()
    agent.log("生成代码:")
    for step in plan:
        res = agent.step(step)
        agent.log(res)


if __name__ == '__main__':
    # run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，并向其中写入内容 'hello'，最后关闭文件")
    # run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，获取该文档的路径，最后关闭文档")
    # run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，选中第三行到第五行，并进行剪切，在文本开始处粘贴，并将文档另存为 'C:\\Users\\21972\\Desktop\\temp2.docx'，最后关闭文档")
    # run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，选中第三行到第五行，并进行剪切，最后关闭文档")
    # run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，保存文档为PDF文件 'C:\\Users\\21972\\Desktop\\temp.pdf'，最后关闭文档")  # 转换之后pdf损坏
    run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，将光标移动到第一行第五个字符，写入内容 'world'，最后关闭文件")
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
    run_task("请帮我打开文档 'C:\\Users\\21972\\Desktop\\temp.docx'，获取该文档的路径，最后关闭文档")

from tbot.agent import TBotAgent
from utils.capture import capture


def run_task(task):
    agent = TBotAgent(task)
    plan = agent.plan()
    agent.log("生成代码:")
    for step in plan:
        res = agent.step(step)
        agent.log(res)


if __name__ == '__main__':
    code, res = capture("winword")
    run_task("请帮我打开文档 'C:\\Users\\lornd\\Desktop\\res.docx'，并向其中写入内容 'hello'，最后关闭文件")

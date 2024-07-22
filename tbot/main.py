from tbot.agent import TBotAgent
from utils.autotest.autotest import run_test


def run_task(task):
    agent = TBotAgent(task)
    _ = agent.generate_plan()
    code = agent.generate_code()
    agent.log("生成代码:")
    agent.log(code)
    run_test(code)


if __name__ == '__main__':
    # code, res = capture("winword")
    run_task('获取鼠标的位置')
    # run_task('请帮我打开文档 "C:\\Users\\lornd\\Desktop\\TBot\\origin.docx" 和文档 "C:\\Users\\lornd\\Desktop\\TBot\\res.docx"，并将 origin.docx 中的所有内容复制到 res.docx 中')
    # run_task("请帮我打开文档 'C:\\Users\\lornd\\Desktop\\res.docx'，并向其中写入内容 'hello'，最后关闭文件")

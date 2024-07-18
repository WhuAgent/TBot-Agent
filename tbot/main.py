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
    run_task('请帮我在激活记事本中激活1.txt这个窗口，判断它是否存在，最大化这个窗口，查看这个时候窗口的大小，将其改到宽1000，高800.然后移动这个窗口到x坐标为0，y坐标为10的位置，将他置顶，获取窗口名称、类名、路径、进程，最后关闭这个窗口')
    # run_task("请帮我打开文档 'C:\\Users\\lornd\\Desktop\\res.docx'，并向其中写入内容 'hello'，最后关闭文件")

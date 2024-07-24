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
    run_task(
        '请帮我打开excel表格"C:\\Users\\Martin\\Downloads\\thingo-T-BOT\\Tbot-Agent\\test\\test.xlsx"，'
        '随后激活名称为"价格"的工作表。'
        '在"价格"工作表中执行宏"DeleteEmptyRows"。'
        '接下来，创建一个名称为"价格副本"的工作表，并将该原先"价格"工作表的内容复制到"价格副本"的工作表中。'
        '复制完成以后，删除原先的"价格”工作表。'
        '激活名称为"价格副本"的工作表，读取"A1"到"D5"的全部内容到v_DataTable中，首行是数据表的列名，'
        '将数据表v_DataTable写入"价格副本"工作表中，写入的起始地址为"A6"。'
        # '筛选当前"价格副本"工作表中的列名为"合计"的数据v_Ret，并将数据表v_Ret写入"价格副本"工作表中，写入的起始地址为"E2"'
    )
    # run_task("请帮我打开文档 'C:\\Users\\lornd\\Desktop\\res.docx'，并向其中写入内容 'hello'，最后关闭文件")

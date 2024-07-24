from tbot.main import run_task


def test_excel():
    run_task(
        '请帮我打开excel表格"C:\\Users\\Martin\\Downloads\\thingo-T-BOT\\Tbot-Agent\\test\\test.xlsx"，'
        '随后激活名称为"价格"的工作表，'
        '在"价格"工作表中执行宏DeleteEmptyRows'
        '接下来，创建一个名称为"价格副本"的工作表，并将该原先"价格"工作表的内容复制到"价格副本"的工作表中。'
        '复制完成以后，删除原先的"价格”工作表。'
        '激活名称为"价格副本"的工作表，读取"A1"到"D5"的全部内容到v_DataTable中，注意，首行是数据表的列名'
        '将数据表v_DataTable写入"价格副本"工作表中'
    )

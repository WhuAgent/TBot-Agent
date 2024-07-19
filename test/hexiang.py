from tbot.main import run_task
def test_excel():
    run_task('获取当前工作表，创建一个新工作表TestSheet并切换到该工作表，'
             '在TestSheet的"A1"列写入数据[1, 2, 3, 4, 5]，'
             '读取TestSheet的"A1"列的数据，'
             '在TestSheet的"B1"列插入一个新列[6, 7, 8, 9, 10]，'
             '获取TestSheet的总行数和总列数，'
             '合并TestSheet的"A1:B1"单元格，'
             '设置TestSheet的"B1"列宽度为20，'
             '设置TestSheet的"A2"行行高为25，'
             '设置TestSheet的A1单元格背景颜色为黄色，'
             '设置TestSheet的A1单元格字体颜色为红色，'
             '获取TestSheet的A1单元格字体颜色,'
             '获取所有工作表名,'
             '将TestSheet重命名为FinalSheet。')
    # ExcelOpenWorkbook("C:\\Users\\Xifeng\\Desktop\\test.xlsx",“是”,“0”,“0”,“false”)
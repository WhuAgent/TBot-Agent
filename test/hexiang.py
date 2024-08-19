from tbot.main import run_task


def test_excel():
    run_task('获取当前工作表，创建一个新工作表TestSheet并切换到该工作表，'
             '在TestSheet的"A1"列写入数据[1, 2, 3, 4, 5]，'
             '在TestSheet的"D1"列写入数据[1, 2, 3, 4, 5]，'
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
             '删除TestSheet的"E"列数据，'
             '将TestSheet重命名为FinalSheet。')
    # 需要自行在t-bot中开头添加如下代码（文件路径自行更换）
    # Dim excel_object = ""
    # excel_object = ExcelOpenWorkbook("C:\\Users\\Xifeng\\Desktop\\test.xlsx","是","0","0","false","excel对象","false")


def test_file():
    run_task('在"D:\\Test_T_Bot"下创建一个新的文件夹"test_folder",'
             '复制文件“D:\\Test_T_Bot\\test_file.txt”到test_folder文件夹,'
             '在文件"test_file.txt"中写入数据"你好，世界！",'
             '读取test_file.txt中的数据，'
             '获取test_file.txt的文件名'
             '获取test_file.txt的扩展名,'
             '获取test_file.txt的父级路径,'
             '获取test_file.txt的文件大小,'
             '获取test_folder的文件夹大小,'
             '在"D:\\Test_T_Bot"下创建一个新的文件夹"copy_test_folder",'
             '复制test_folder到copy_test_folder,'
             '重命名test_file.txt为"renamed_test_file.txt",'
             '删除renamed_test_file.txt,'
             '删除copy_test_folder文件夹,'
             '判断test_file.txt是否存在,'
             '判断test_folder是否存在。')
    # 需要在目录下放置test_file.txt文件，因为没有创建文件的功能
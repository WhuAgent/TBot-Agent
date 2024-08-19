from tbot.main import run_task


def test_excel():
    run_task('请帮我打开Excel工作簿文件 "C:\\Users\\12423\\Desktop\\res.xls" ')
    # run_task("请帮我打开Excel工作簿 'F:/res.xls'，将“你好”写入到sheet1工作表中的A2单元格，另存到'F:\\finalres.xls'，关闭文件")

def test_excel_selectdata():
    # 5.查找数据
    run_task("请帮我打开Excel工作簿 'C:\\Users\\12423\\Desktop\\res.xls',在sheet1中A1:G10中查找'nihao'")
    #再加一个PrintLogToForm("v_Ret","0","0",false)

def test_excel_readcell():
    # 6.读取单元格
    run_task("请帮我打开Excel工作簿 'C:\\Users\\12423\\Desktop\\res.xls',在sheet1中读取B3单元格的值")#再加一个PrintLogToForm("v_Ret","0","0",false)

def test_excel_setcell():
    # 7.写入单元格
    run_task("请帮我打开Excel工作簿 'F:/res.xls',将“你好”写入到sheet1工作表中的A2单元格")

def test_excel_getrange():
    # 8.读取区域
    run_task("请帮我打开Excel工作簿 'F:/res.xls',在sheet1中读取A2:B3区域的值")#PrintLogToForm(v_Array,"0","0","false")

def test_excel_setselectarea():
    # 9.写入区域
    run_task("请帮我打开Excel工作簿 'F:/res.xls',将[[你好,""],["",nihao]]写入sheet1中A5区域")

def test_excel_cleararea():
    # 10.清除区域
    run_task("请帮我打开Excel工作簿 'F:/res.xls',清除工作表sheet1中A5:B6区域")

def test_excel_deletearea():
    # 11.删除区域
    run_task("请帮我打开Excel工作簿 'F:/res.xls',删除sheet1中A5:B6区域")

def test_excel_getrowdata():
    # 12.读取行
    run_task("请帮我打开Excel工作簿 'F:/res.xls',读取sheet1中B3单元格后的行,返回数组")   #PrintLogToForm(v_Array,"0","0","false")  #？？？？会读到单元格

def test_excel_setrow():
    # 13.写入行（跟提示词一样写”一行数组就可以了“  （就算感觉不通顺也按照那个提示词对函数说明写，就能识别到））
    run_task("请帮我打开Excel工作簿 'F:/res.xls',从sheet1中A5写入一行数组[你好,nihao]")

def test_excel_insertrow():
    # 14.插入行
    run_task("请帮我打开Excel工作簿 'F:/res.xls',将数组[你好,nihao]插入到sheet1中A1单元格对应的行之上")

def test_excel_deleterow():
    # 15.删除行
    run_task("请帮我打开Excel工作簿 'F:/res.xls',从sheet1中 '删除' A5 所在行,关闭Excel工作簿")

def test_excel_mixsituation():
    run_task("请帮我打开Excel工作簿 'C:\\Users\\12423\\Desktop\\res.xls',将数组[你好,nihao]插入到sheet1中A1单元格对应的行之上,读取sheet1中A1单元格后的行,返回数组，将数组写入到sheet1工作表中的A2单元格,关闭Excel工作簿")


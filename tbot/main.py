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
    # run_task('请帮我打开文档 "C:\\Users\\lornd\\Desktop\\TBot\\origin.docx" 和文档 "C:\\Users\\lornd\\Desktop\\TBot\\res.docx"，并将 origin.docx 中的所有内容复制到 res.docx 中')

    # run_task("请帮我打开Excel工作簿 'F:/res.xls'，将“你好”写入到sheet1工作表中的A2单元格，另存到'F:\\finalres.xls'，关闭文件")
    # 5.查找数据
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',在sheet1中A1:G10中查找'nihao'")#再加一个PrintLogToForm("v_Ret","0","0",false)

    # 6.读取单元格
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',在sheet1中读取B3单元格的值")#再加一个PrintLogToForm("v_Ret","0","0",false)

    # 7.写入单元格
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',将“你好”写入到sheet1工作表中的A2单元格")

    # 8.读取区域
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',在sheet1中读取A2:B3区域的值")#PrintLogToForm(v_Array,"0","0","false")

    # 9.写入区域
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',将[[你好,""],["",nihao]]写入sheet1中A5区域")

    # 10.清除区域
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',清除sheet1中A5:B6区域")

    # 11.删除区域
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',删除sheet1中A5:B6区域")

    # 12.读取行
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',读取sheet1中B3单元格后的行,返回数组")   #PrintLogToForm(v_Array,"0","0","false")  #？？？？会读到单元格

    # 13.写入行（跟提示词一样写”一行数组就可以了“  （就算感觉不通顺也按照那个提示词对函数说明写，就能识别到））
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',从sheet1中A5写入一行数组[你好,nihao]")

    # 14.插入行
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',将数组[你好,nihao]插入到sheet1中A1单元格对应的行之上")

    # 15.删除行
    run_task("请帮我打开Excel工作簿 'F:/res.xls',从sheet1中 '删除' A5 所在行,关闭Excel工作簿")

    
    # run_task("请帮我打开Excel工作簿 'F:/res.xls',从sheet1中 '删除' A5 所在行,关闭Excel工作簿")

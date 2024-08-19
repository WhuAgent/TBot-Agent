from tbot.main import run_task


def test_exists():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，检测该文档是否存在')

def test_add():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，并添加新的Word文档，之后关闭该文档')

def test_selectLine_and_cut():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，选中文档第1行到第3行的内容，'
             '进行剪切，之后进行保存，最后关闭该文档')

def test_exportPDF():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，'
             '保存为PDF文件到C:\\Users\\21972\\Desktop\\temp.pdf，'
             '最后关闭该文档')

def test_getFilePath():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，'
             '得到该文档的位置,'
             '最后关闭该文档')

def test_moveCursor():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，'
             '将光标向下移动三行，'
             '最后关闭该文档')

def test_selectAll():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，'
             '选中文档的全部内容，'
             '最后关闭该文档')

def test_setSelectTextContentPosition():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，'
             '查找内容为 hello 的字符串之后将光标移动到查找内容之后，'
             '最后关闭该文档')

def test_overRead():
    run_task('请帮我打开文档 "C:\\Users\\21972\\Desktop\\temp.docx"，'
             '对文档重新写入内容为 "hello"的字符串，'
             '最后关闭该文档')
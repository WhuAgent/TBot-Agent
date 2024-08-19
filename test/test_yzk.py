from tbot.main import run_task


def test_close():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，然后关闭文档')


def test_delete():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，删除一个字符，最后关闭文件')


def test_enter():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，插入一个回车，最后关闭文件')


def test_insert_page():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，插入一个新的页面，最后关闭文件')


def test_insert_image():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，插入图片 "C:\\Users\\HP\\Desktop\\tmp.jpg"，最后关闭文件')


def test_read():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，读取选中内容，最后关闭文件')


def test_append_text():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，写入字体为宋体、字号为12的“你好”，最后关闭文件')


def test_replace():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，将其中的文字你替换为文字您，最后关闭文件')


def test_font_name():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，将选中区域设置为宋体，最后关闭文件')


def test_font_size():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，将选中区域的文字大小设置为12，最后关闭文件')


def test_font_color():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，将选中区域的文字的颜色设置为红色，最后关闭文件')


def test_font_style():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，为选中区域添加波浪线，最后关闭文件')


def test_font_alignment():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，将选中区域设置为靠中间对齐，最后关闭文件')


def test_check_exist():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，检测该文档是否存在，最后关闭文件')


def test_datatable():
    run_task('请帮我打开文档 "C:\\Users\\HP\\Desktop\\res.docx"，添加一个名字为"new"的DataTable，最后关闭文件')




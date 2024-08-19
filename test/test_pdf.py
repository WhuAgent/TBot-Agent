from tbot.main import run_task

def test_pdf():
    run_task('获取“C:\\Users\\19101\\Desktop\\test_pdf\\2.pdf”的总页数和所有图片,获取第一页中的图片'
    '合并“C:\\Users\\19101\\Desktop\\test_pdf\\2.pdf”和“C:\\Users\\19101\\Desktop\\test_pdf\\3.pdf”,合并后的文件保存在同文件夹下,命名为m.pdf'
    '加密“C:\\Users\\19101\\Desktop\\test_pdf\\3.pdf”,密码为123456')

def test_GetPDFAllPicture():
    run_task('获取“C:\\Users\\19101\\Desktop\\test_pdf\\2.pdf”的总页数和所有图片')

def test_GetAppointPage():
    run_task('获取“C:\\Users\\19101\\Desktop\\test_pdf\\2.pdf”中第二页的文字')

def test_PDFToPicture():
    run_task('将“C:\\Users\\19101\\Desktop\\test_pdf\\2.pdf”的第一页另存为图片')

if __name__ == '__main__':
    #test_pdf()
    #test_PDFToPicture()
    test_GetPDFAllPicture()
    #test_GetAppointPage()

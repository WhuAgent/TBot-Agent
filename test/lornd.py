from tbot.main import run_task


def test_document():
    run_task('请帮我打开文档 "C:\\Users\\lornd\\Desktop\\TBot\\origin.docx" '
             '和文档 "C:\\Users\\lornd\\Desktop\\TBot\\res.docx"，并将 origin.docx 中的所有内容复制到 res.docx 中')

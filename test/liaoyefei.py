from tbot.main import run_task


def test_file():
    run_task('检测文件"D:\\Awork\\AI-agent\\rpa-test\\test.csv"是否存在，'
             '获取文件夹"D:\\Awork\\AI-agent\\rpa-test"文件列表，'
             '获取文件夹"D:\\Awork\\AI-agent\\rpa-test"文件夹列表，'
             '读取"D:\\Awork\\AI-agent\\rpa-test\\test.csv"中的数据，'
             '压缩"D:\\Awork\\AI-agent\\rpa-test\\test.csv"文件到文件夹"D:\\Awork\\AI-agent\\rpa-test"，'
             '压缩"D:\\Awork\\AI-agent\\rpa-test\\test"文件夹到文件夹"D:\\Awork\\AI-agent\\rpa-test"，'
             '重命名"D:\\Awork\\AI-agent\\rpa-test\\test"为"666",'
             )


def test_system():
    run_task('执行powershell 命令calc , '
             '执行命令行 calc,'
             '获取系统文件夹路径,'
             '获取用户文件夹路径,'
             '获取临时文件夹路径,'
             '锁屏'
             )

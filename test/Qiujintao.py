# -*- coding:utf-8 -*-
"""
作者：86173
日期：2024年07月23日
"""
from tbot.main import run_task


def test_document():
    run_task('请帮我打开计算器，计算器路径是"C:\\Windows\\System32\\calc.exe"；'
             '之后执行关闭计算器进程命令；'
             '我要在路径"C:\\Users\\86173\\Desktop"下选择文件；'
             '之后我要进行文件夹的选择；'
             '尝试获取用户的输入；'
             '弹出警告提示框，警告用户有违法操作；'
             '为我剪贴板设置文本”hello world“，并读取剪贴板的内容；'
             '在屏幕中间写"hell0\nw0rld",字体天蓝色大小50,四秒后清除内容；'
             '为我锁屏')
    # run_task('请帮我打开计算器，计算器路径是"C:\\Windows\\System32\\calc.exe"，之后再关闭计算器')
    # run_task('请帮我打开网易云音乐，其路径是""C:\\Program Files (x86)\\NetEase\\CloudMusic\\cloudmusic.exe""')
    # run_task('弹出警告提示框，警告用户有违法操作')
    # run_task('我要使用选择文件的命令，在路径"C:\\Users\\86173\\图片"下选择文件')
    # run_task('我要选择文件夹')
    # run_task('尝试获取用户的输入')
    # run_task('为我剪贴板设置文本”hello world“，并读取剪贴板的内容')
    # run_task("在屏幕中间写'hell0\nw0rld',字体天蓝色大小50,四秒后清除内容")
    # run_task('为我锁屏')
    # run_task('自定义一个对话框，需要用户输入账号和密码')
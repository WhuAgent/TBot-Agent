from tbot.main import run_task

def test_text():
    run_task('判断“百度”是否存在，通过“搜索”获得界面元素，获得组一中的文字，鼠标点击“百度”，鼠标移动到“搜索”')


if __name__ == '__main__':
    test_text()
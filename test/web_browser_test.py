from tbot.main import run_task


def test_web_browser_create():
    run_task(
        "请帮我创建一个Msedge浏览器实例，并打开百度")


def test_web_browser_bind():
    run_task(
        "请帮我绑定已有的Msedge浏览器实例")


def test_web_browser_get_status():
    run_task(
        "请帮我创建一个Msedge实例，获取Msedge浏览器实例的状态")


def test_web_browser_new_tab():
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com'")


def test_web_browser_active_tab():
    # todo: 无法切换标签页
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',再打开'www.bilibili.com'，切换到百度网站标签页")


def test_web_browser_get_html():
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',获取当前网页的HTML代码，然后将其打印到调试信息")


def test_web_browser_reload():
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',然后刷新当前网页")


def test_web_browser_close_tab():
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',然后关闭当前标签页")


def test_web_browser_run_js():
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',然后运行js代码 'alert(\"hello\")'")


def test_web_browser_take_screenshot():
    # todo: 无法截图
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',然后截取当前网页的屏幕截图，保存到 'E:\\temp\\screenshot.png'")


def test_web_browser_get_title():
    run_task(
        "请帮我在Msedge浏览器中打开网页 'https://www.baidu.com',获取当前网页的标题")


if __name__ == '__main__':
    test_web_browser_create()

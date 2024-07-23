from tbot.main import run_task


def test_screen():
    # 将每一步的结果输出在下一步开始前输出
    # 在每一步结束后输出其结果
    # 将每一步的结果输出在每一步结束后输出
    # 将每一步的返回值在下一步开始前输出
    # 将具有返回值的步骤在下一步开始前输出
    #
    run_task('对于Google Chrome股票列表，获取其句柄，判断其是否存在，输出变量，获取其所有子元素，输出变量，获取其父四级的所有父元素，输出变量')


def test_screen_GetElementCheck():
    run_task('对于Github setting复选框。获取其句柄，判断其是否被勾选，输出变量，设置其为勾选。')


def test_screen_ElementSelect():
    run_task('对于excel列表。获取其句柄，获取其中所有的未选择项，输出这些未选择项，将其中索引为[4,5]的设为选择项。')


def test_Screen_ElementAttribute():
    run_task('对于百度搜索框。获取其句柄，获取其中设置其中value属性值为"hello world"，获取其属性value的值，输出此属性值。')


def test_Screen_ElementValue():
    run_task('对于百度搜索框。获取其句柄，获取其文本内容并输出此属性值，设置文本内容为"hello world"，获取其文本内容输出此属性值。')


def test_Screen_ElementRect():
    run_task('对于百度搜索框。获取其句柄，获取其区域位置并输出此属性值。')


def test_Screen_ElementTakeShot():
    run_task('对于百度搜索框。获取其句柄，对其截图保存到"D:\\myScreenshot.png"。')


def test_Screen_WaitForElement():
    run_task('对于百度搜索框。获取其句柄，等待其能在5秒内能够看见，将得到的变量输出到控制台"。')


def test_Screen_GetElementTable():
    run_task('对于Google Chrome股票列表，获取其句柄，提取其中数据表，输出提出的数据表')


def test_Screen_GetBatchData_single():
    # 当前页
    run_task('获取Google Chrome股票列表的句柄，批量提取股票列表中其中当前页的数据，将提取到的数据输出')


def test_Screen_GetBatchData_multiple():
    # 全部
    # 五页
    run_task('获取Google Chrome股票列表的句柄，获取下一页按钮句柄，批量提取股票列表中其中所有的数据，将提取到的数据输出')


def test_Screen_ScreenShot():
    run_task('对屏幕进行截图，将截图保存到"D:\\myScreenshot.png')
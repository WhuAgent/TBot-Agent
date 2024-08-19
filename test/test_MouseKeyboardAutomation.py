from tbot.main import run_task

# 模拟鼠标移动到指定位置
# 根据句柄找目标元素存在问题：如果Google Chrome中有打开的网页，仅通过Google Chrome无法找到目标
def test_SendTargetMouseMove():
    run_task('请把鼠标光标移到任务栏的Google Chrome上')

# 获取鼠标位置
def test_GetMousePoint():
    run_task('获取鼠标的位置')

# 模拟鼠标拖动
def test_MouseDrag():
    # run_task('请把鼠标从("20","20")移到("200","200")')
    run_task('模拟鼠标的移动，起点为("20","20")，终点为("400","400")')

# 模拟鼠标滚动
def test_MouseWheel():
    run_task('模拟鼠标向后滚动10次')

# 模拟鼠标点击
def test_SendMouseClick():
    run_task('鼠标点击')

# 模拟鼠标移动
def test_SendMouseMove():
    run_task('请将鼠标移到横坐标为50，纵坐标为60的位置')

# 点击目标
def test_TargetMouseClick():
    run_task('请点击任务栏中的Google Chrome')

# 在目标中输入
def test_SendTargetKeys():
    run_task('请点击任务栏中的搜索，再在任务栏的搜索框中输入999')

# 在目标中按键
def test_SendTargetAdvancedKeys():
    run_task('请点击任务栏中的搜索，再在任务栏中的搜索框中按下Enter键')

# 模拟输入文本
def test_SendKeys():
    run_task('请输入999')

# 模拟按键
def test_SendAdvancedKeys():
    run_task('请按下Enter键')
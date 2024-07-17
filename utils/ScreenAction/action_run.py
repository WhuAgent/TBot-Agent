import cv2
import pyautogui
import time # 请确保已安装 keyboard 模块
import numpy as np  # 导入 NumPy 库
from pynput.keyboard import Key, Controller

keyboard = Controller()

template_image = cv2.imread('run.png', cv2.IMREAD_GRAYSCALE)  # 模板图像路径
template_width, template_height = template_image.shape[::-1]

#     print("开始模板匹配")

# 获取当前屏幕截图
screen_shot = pyautogui.screenshot()
screen_image = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2GRAY)

# 在屏幕截图中搜索模板
result = cv2.matchTemplate(screen_image, template_image, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 如果匹配值大于某个阈值，认为找到了模板
threshold = 0.8
if max_val >= threshold:
    # 计算点击位置
    click_x, click_y = max_loc[0] + template_width / 2, max_loc[1] + template_height / 2
    pyautogui.click(click_x, click_y)



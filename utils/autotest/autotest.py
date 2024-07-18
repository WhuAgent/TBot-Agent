import os
import cv2
import pyautogui
import numpy as np
from pynput.keyboard import Key, Controller

from PIL import Image, ImageDraw

pynput = Controller()


def get_target_element(image_path):
    # 获取模板图像
    template_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template_width, template_height = template_image.shape[::-1]

    # 获取当前屏幕截图
    screen_shot = pyautogui.screenshot()
    screen_image = cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2GRAY)

    # 在屏幕截图中搜索模板
    result = cv2.matchTemplate(screen_image, template_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 匹配程度阈值
    threshold = 0.8
    # print(max_val)

    return (max_loc, (template_width, template_height), screen_shot) if max_val >= threshold else None


def click(screen_shot, top_left, shape, offset_x=0, offset_y=0):
    click_x = top_left[0] + shape[0] / 2 + offset_x
    click_y = top_left[1] + shape[1] / 2 + offset_y

    # draw = ImageDraw.Draw(screen_shot)
    # draw.rectangle([click_x-10, click_y-10, click_x+10, click_y+10], fill='red')
    # screen_shot.show()
    pyautogui.click(click_x + offset_x, click_y + offset_y)


def open_tbot():
    template_root = "utils/autotest/templates/open_tbot"
    for root, dirs, files in os.walk(template_root):
        for file in files:
            image_path = os.path.join(root, file)
            if res := get_target_element(image_path):
                click(res[2], top_left=res[0], shape=res[1])


def input_code(code):
    template_root = "utils/autotest/templates/input_code"
    for root, dirs, files in os.walk(template_root):
        for file in files:
            image_path = os.path.join(root, file)
            if res := get_target_element(image_path):
                click(res[2], top_left=res[0], shape=res[1], offset_y=150)

                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press("backspace")
                pynput.type(code)


def run():
    template_root = "utils/autotest/templates/run"
    for root, dirs, files in os.walk(template_root):
        for file in files:
            image_path = os.path.join(root, file)
            if res := get_target_element(image_path):
                click(res[2], top_left=res[0], shape=res[1])


def run_test(code):
    open_tbot()
    input_code(code)
    run()

import json
import os
from lxml import html

from selenium.webdriver.common.by import By

from model.html_parser.config import form_data_parser_map
from utils.logger import Logger
from model.utils import get_prompts, get_webdriver, html_status2description
from model.exceptions import FailedError

ignored_tags = ["br"]
form_elements = ["select", "input", "textarea"]


def parse_action(action):
    # delimiters = "(|)|,"
    # regex_pattern = re.compile(delimiters)
    # action = regex_pattern.split(action)
    # action_name = action[0]
    # args = action[1:] if len(action) > 1 else []
    action_data = json.loads(action)
    return {
        "action": action_data.get("action"),
        "args": action_data.get("args")
    }


def check(element, tag, content, **attribute):
    if element.tag != tag:
        return False
    if content and element.text != content:
        return False
    for key, value in attribute.items():
        if key in ["class", "Class"]:
            class_names = value.split(",") if isinstance(value, str) else value
            for class_name in class_names:
                element_class = element.get("class").split(",")
                element_class = [ele.strip() for ele in element_class]
                if class_name.strip() not in element_class:
                    return False
        elif element.get(key) != value:
            return False
    return True


def find(father, exclude_child, tag, content, **attribute):
    if check(father, tag, content, **attribute):
        return [father]
    res = []
    for child in father:
        if child == exclude_child:
            continue
        if data := find(child, None, tag, content, **attribute):
            res.extend(data)
    return res if len(res) > 0 else None


def generate_observation(template, **kwargs):
    return template.format(**kwargs)


class MiniWobAgent:

    def __init__(self, env_name, logger_prefix=""):
        self.env_name = env_name
        logging_root = f"log/{env_name}"
        self.logger = Logger(logging_root, logger_prefix)

        self.driver = get_webdriver()
        self.playground = None  # 智能体操作浏览器的区域
        self.task = None  # 智能体需要完成的任务
        self.extra_attributes = []  # 智能体需要额外关注的属性
        self.html_status = None  # 网页中各种元素的状态，方便智能体进行操作
        self.html_description = None  # 网页中各种元素的状态，方便 LLM 进行解读
        self.form_elements_in_html = []  # 网页中的表单元素（有值但是其值不在 html 源代码中体现）
        self.form_data_status = None  # 网页中表单元素值的状态
        self.ref_id = 0
        self.found_ref_ids = None
        self.start()
        self.system_prompt, self.task_prompt = get_prompts(self.task, self.html_description, self.form_data_status)
        self.plan = None
        self.history_action = []

        self.element_found = []

        self.action_func_map = {
            "find_element": self.action_find_element,
            "click": self.action_click,
            "type": self.action_type,
        }

    def start(self):
        miniwob_dir = "C:/Users/lornd/Documents/Projects/WebNavigation/env/miniwob/miniwob_interface/html/miniwob"
        base_url = f"file://{miniwob_dir}"
        url = f"{base_url}/{self.env_name}.html"

        self.driver.get(url)

        self.driver.execute_script("core.startEpisodeReal();")

        extra_attributes_file_path = f"prompt/extra_attributes/{self.env_name}.json"
        extra_attributes_file_path = os.path.join(os.getcwd(), extra_attributes_file_path)
        if os.path.exists(extra_attributes_file_path):
            with open(extra_attributes_file_path, "r", encoding="UTF-8") as f:
                self.extra_attributes = json.load(f)

        return self.obs()

    def obs(self):
        self.task = self.driver.execute_script("return core.getUtterance();")  # 获取当前网页需要做的事情
        self.playground = self.driver.find_element(By.ID, "area")
        self.form_elements_in_html = []
        self.html_status = self.get_html_status(self.playground)
        self.html_description = html_status2description(self.html_status)
        self.get_form_data()

        return self.html_description, self.form_data_status

    def get_html_status(self, element):
        if element.tag_name in ignored_tags or not element.is_displayed():
            return None
        if element.tag_name in form_elements:
            self.form_elements_in_html.append(element)
        has_children = self.driver.execute_script("return arguments[0].children.length > 0;", element)
        if not element.get_attribute("ref"):
            self.driver.execute_script("arguments[0].setAttribute('ref', arguments[1]);", element, self.ref_id)
            self.ref_id += 1

        status = {
            "tag": element.tag_name,
            "ref": element.get_attribute("ref"),
            "element": element,
        }
        if element.get_attribute("class") and len(element.get_attribute("class")) > 0:
            status["class"] = element.get_attribute("class").split(",")

        if has_children:
            all_child_elements = element.find_elements(By.XPATH, "./*")
            children_status = []

            for child in all_child_elements:
                child_status = self.get_html_status(child)
                if child_status is not None:
                    children_status.append(child_status)

            status["children"] = children_status
            return status
        else:
            if element.text != "":
                status["content"] = element.text
            for attribute in self.extra_attributes:
                if element.get_attribute(attribute):
                    status[attribute] = element.get_attribute(attribute)
            return status

    def get_form_data(self):
        self.form_data_status = []
        for element in self.form_elements_in_html:
            data = form_data_parser_map[element.tag_name](element)
            self.form_data_status.append(data)

    def step(self, action):
        action_name = action.get("action")
        args = action.get("args")

        config_path = f"model/action_observation_config/{action_name}.json"
        with open(config_path, "r", encoding="UTF-8") as f:
            config = json.load(f)

        try:
            result = self.action_func_map[action_name](args)
        except Exception as e:
            observation = generate_observation(config[str(type(e).__name__)])
        else:
            observation = generate_observation(config["Success"], **result)

        metadata = self.get_metadata()
        reward = metadata.get("raw_reward")
        done = metadata.get("done")
        info = metadata.get("reason")

        return observation, reward, done, info

    def get_metadata(self):
        """Get other metadata.

        Returns:
            dict with the following keys:
            - done (bool)
            - env_reward (float; only well-defined when done is True):
                Environment-defined reward, possibly scaled by time
            - raw_reward (float; only well-defined when done is True):
                Environment-defined reward, NOT scaled by time
            - reason (any): reason for giving the reward (for debugging);
                will likely be None if done is False
        """
        return self.driver.execute_script(
            "return {"
            '"done": WOB_DONE_GLOBAL,'
            '"env_reward": WOB_REWARD_GLOBAL,'
            '"raw_reward": WOB_RAW_REWARD_GLOBAL,'
            '"reason": WOB_REWARD_REASON,'
            "};"
        )

    # TODO: 将动作部分从 Agent 类中抽离出去
    def action_find_element(self, args):
        start_ref_id = args.get("start_ref_id")
        tag = args.get("tag")
        content = args.get("content")
        attribute = args.get("attribute")
        found_ref_ids = self.find_element(start_ref_id, tag, content, **attribute if attribute else {})
        if found_ref_ids:
            return {
                "found_ref_ids": found_ref_ids
            }
        else:
            raise FailedError

    def find_element(self, start_ref_id, tag, content, **attribute):
        """
        寻找所有满足条件为 condition ，且与 element_from 的最近公共祖先（LCA）最深的元素。
        其中：
        element_from 以 path 的形式给出
        condition 以 lambda 表达式的形式表示寻找元素的条件。
        """
        dom = html.fromstring(self.playground.get_attribute("outerHTML"))
        child = None
        start_element = dom.xpath(f"//*[@ref='{start_ref_id}']")[0]
        while start_element is not None:
            if res := find(start_element, child, tag, content, **attribute):
                self.found_ref_ids = [element.get("ref") for element in res]
                return self.found_ref_ids
            child = start_element
            start_element = start_element.getparent()
        return None

    def action_click(self, args):
        self.click()
        html_description, form_data_status = self.obs()
        html_description = json.dumps(html_description, indent=4)
        form_data_status = json.dumps(form_data_status, indent=4)
        return {
            "html_description": html_description,
            "form_data_status": form_data_status,
        }

    def click(self):
        """
        点击元素 element。
        """
        for ref_id in self.found_ref_ids:
            element = self.driver.find_element(By.XPATH, f"//*[@ref='{ref_id}']")
            element.click()
        self.element_found = []

    def action_type(self, args):
        content = args.get("content")
        self.type(content)
        _, form_data_status = self.obs()
        form_data_status = json.dumps(form_data_status, indent=4)
        return {
            "form_data_status": form_data_status
        }

    def type(self, content):
        """
        清空元素 element 原有内容，并输入内容 content。
        """
        ref_id = self.found_ref_ids
        element = self.driver.find_element(By.XPATH, f"//*[@ref='{ref_id}']")
        element.clear()
        element.send_keys(content)

    def log(self, content):
        self.logger.log(content)

    def close(self):
        self.driver.quit()

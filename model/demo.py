from model.ours.agent import MiniWobAgent
from model.ours.main import action2func_call


def click_shades():
    env_name = "click-shades"
    agent = MiniWobAgent(env_name, "demo")

    task = agent.task
    target_color = task.split(" ")[5]

    agent.log(f"task: {task}")
    agent.log(agent.html_description)
    agent.log(agent.form_data_status)

    agent.log(f"Action: agent.find_element(0, 'span', '', **{{'data-color': {target_color} }})")
    found_elements = agent.find_element(0, "span", "", **{"data-color": target_color})
    agent.log(f"Found elements: {found_elements}")

    agent.log(f"Action: agent.click()")
    agent.click()
    html_description, form_data_status = agent.obs()
    agent.log(html_description)
    agent.log(form_data_status)

    agent.log(f"Action: agent.find_element(0, 'button', 'Submit')")
    found_elements_2 = agent.find_element(0, "button", "Submit")
    agent.log(f"Found elements: {found_elements_2}")

    agent.log(f"Action: agent.click()")
    agent.click()

    agent.close()


def social_media():
    env_name = "social-media"
    agent = MiniWobAgent(env_name, "demo")

    task = agent.task


def test():
    env_name = "choose-list"
    agent = MiniWobAgent(env_name, "test-check")

    action = {
        "action": "find_element",
        "args": {
            "start_ref_id": 7,
            "tag": "button",
            "content": "Submit",
            "attribute": {"class": ["secondary-action"]}
        }
    }

    action = {
        "action": "click"
    }
    # func_call = action2func_call(action)
    print(agent.step(action))
    # agent.find_element(start_ref_id=0, tag="button", content="Submit", attribute={'class': ['secondary-action']})


if __name__ == '__main__':
    # click_shades()
    test()

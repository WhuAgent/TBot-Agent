from selenium.webdriver.support.ui import Select


def parse_select(element):
    select = Select(element)
    selected_option = select.first_selected_option
    return {
        "tag": element.tag_name,
        "value": selected_option.text
    }


def parse_input(element):
    return {
        "tag": element.tag_name,
        "value": element.get_attribute('value')
    }

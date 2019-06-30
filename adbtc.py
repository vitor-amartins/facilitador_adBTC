import time
import json

import pyautogui
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def save_captchas():
    with open('captchas.json', 'w') as json_file:
        json.dump(captchas, json_file)


def get_captchas():
    with open('captchas.json') as json_file:
        return json.load(json_file)


browser = webdriver.Chrome()
browser.maximize_window()
captchas = get_captchas()


def gel(selector):
    return browser.find_element_by_css_selector(selector)


def gels(selector):
    return browser.find_elements_by_css_selector(selector)


def fill_inputs(selector, value):
    inputs = gels(selector)
    for input_ in inputs:
        try:
            input_.send_keys(value)
        except:
            pass


def handle_captcha(imgs_selector, result_inputs_selector, submit_btn_selector):
    imgs = gels(imgs_selector)
    result = ''
    for img in imgs:
        name = img.get_attribute('src').split('/')[-1]
        value = str(input("Digite o valor da imagem: "))
        print(name, value)
        captchas[name] = value
        save_captchas()
        result += value
    result = str(eval(str(result)))
    fill_inputs(result_inputs_selector, result)
    gel(submit_btn_selector).click()
    time.sleep(2)


def login():
    browser.get("https://adbtc.top/index/enter")
    gel("input#addr").send_keys(config("EMAIL"))
    gel("input#secret").send_keys(config("PASSWORD"))
    imgs_selector = '#index-banner > div > div > form > div.row.nopad img'
    result_input_selector = 'input#number'
    submit_btn_selector = 'input#submit_btn'
    handle_captcha(imgs_selector, result_input_selector, submit_btn_selector)
    browser.get('https://adbtc.top/surf/rotator')


def prepare():
    imgs_selector = 'body > div.row > div.col.s12.m9 > form > div:nth-child(2) > div.col.s12.l7.m9 > div:nth-child(2) > div img'
    result_input_selector = 'body > div.row > div.col.s12.m9 > form > div:nth-child(2) > div.col.s12.l7.m9 > div:nth-child(3) > div input'
    submit_btn_selector = 'body > div.row > div.col.s12.m9 > form > div:nth-child(2) > div.col.s12.l7.m9 > input.btn'
    try:
        handle_captcha(imgs_selector, result_input_selector, submit_btn_selector)
    except:
        browser.refresh()
        return


def is_done():
    try:
        if ('watched' in gel('body > div.row > div.col.s12.m9 > h3').text):
            return True
        return False
    except:
        return False


def play():
    try:
        p_info = gels('body > div.row > div.col.s12.m9 > div.card-panel > p')
        start = gel('body > div.row > div.col.s12.m9 > div.card-panel a.btn')
        if ('infinite' in start.get_attribute('class')):
            browser.refresh()
            return
        time_to_wait = p_info[0].text.split('\n')[0].split('|')[1].split(' ')[1]
        main_window = browser.current_window_handle
        start.click()
        time.sleep(int(time_to_wait) + 5)
        browser.switch_to.window(browser.window_handles[0])
        pyautogui.click(x=471, y=16)
    except Exception as e:
        print(e)
        return not(is_done())
        input('Enter to continue...')
        prepare()


login()
prepare()
while (play()):
    time.sleep(5)
print('Done all')
browser.close()

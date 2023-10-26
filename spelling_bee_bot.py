from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import string
from datamuse import datamuse
from selenium.webdriver.common.keys import Keys
import time
api = datamuse.Datamuse()
api.set_max_default(1000)
service = Service("/Users/malcolmhendricks/Development/chromedriver")
service.start()
driver = webdriver.Remote(service.service_url)
driver.get('https://www.nytimes.com/puzzles/spelling-bee')
time.sleep(5)
play = driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/div[2]/div[1]/section[2]/div/div/div/div[2]/div/button[1]')
play.click()

time.sleep(1)
hive = driver.find_element(by=By.CLASS_NAME, value="hive")
optional_letters_html = hive.find_elements(by=By.CLASS_NAME, value="outer")
required_letter = hive.find_element(by=By.CLASS_NAME, value="center").text.lower()
optional_letters = [element.text.lower() for element in optional_letters_html]
page = driver.find_element(by=By.XPATH, value='/html/body')


def generate_params(required, optional):
    parameter = ''
    #exclude letters not in play
    init = ['?', '?', '?', '?', '*', '+', required]
    for letter in optional:
        init.append(letter)
    for i in init:
        parameter += i
    return parameter


params = generate_params(required_letter, optional_letters)
print(params)
word_list = api.words(sp=params)
print(word_list)
words = [info['word'] for info in word_list]
valid_words = []
for word in words:
    if word.count(required_letter) > 0 and word.count(" ") == 0:
        valid_words.append(word)
print(valid_words)
print(words)
for word in valid_words:
    page.send_keys(word)
    page.send_keys(Keys.ENTER)
    for l in range(10):
        page.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)
time.sleep(10)
driver.close()


from selenium import webdriver
from time import sleep

import json

with open("configs.json", "r") as file:
    configs = json.loads(file.read())

print(type(configs))

driver = webdriver.Firefox()
driver.get("https://urionlinejudge.com.br")

elem = driver.find_element_by_name("email")
elem.send_keys(configs["email"])
sleep(0.5)
elem = driver.find_element_by_name("password")
elem.send_keys(configs["password"])
sleep(0.5)
elem = driver.find_element_by_xpath("//input[@value='Sign In']")
elem.click()

elem = driver.find_element_by_xpath("//a[@href='/judge/pt/runs']")
elem.click()
sleep(0.75)

elem = driver.find_element_by_xpath("//option[@value='1']")
elem.click()
sleep(0.85)

elem = driver.find_element_by_xpath("//input[@value='Buscar']")
elem.click()

driver.close()
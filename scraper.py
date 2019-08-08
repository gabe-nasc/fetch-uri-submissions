from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from time import sleep

import json

options = Options()
options.headless = True

with open("configs.json", "r") as file:
    configs = json.loads(file.read())

driver = webdriver.Firefox(options=options)
driver.get("https://urionlinejudge.com.br")
print("Loaded landing page")

elem = driver.find_element_by_name("email")
elem.send_keys(configs["email"])
sleep(0.5)

elem = driver.find_element_by_name("password")
elem.send_keys(configs["password"])
sleep(0.4)

elem = driver.find_element_by_xpath("//input[@value='Sign In']")
elem.click()

print("Signed In")

elem = driver.find_element_by_xpath("//a[@href='/judge/pt/runs']")
elem.click()
sleep(0.35)

print("Listed all submissions")

elem = driver.find_element_by_xpath("//option[@value='1']")
elem.click()
sleep(0.5)

elem = driver.find_element_by_xpath("//input[@value='Buscar']")
elem.click()

print("Listed accepted submissions")

while True:
    print("Scraping", driver.current_url)
    probs_row = driver.find_elements_by_xpath("//td[@class='id']//a")
    submission_ids = [i.text for i in probs_row]
    print(submission_ids, len(submission_ids))

    href = driver.find_element_by_xpath("//a[contains(text(), 'Próximo')]").get_attribute("href").strip()

    if len(href) < 10:
        break
    
    driver.get(href)
    sleep(0.2)

print("Finished")
driver.close()

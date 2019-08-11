from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

import json
import os

# ------ Chrome -------
# The following lines are preferences and configurations
# for the ChromeWebdriver, most of them are attempts at
# disabling the warning for malicious executables since
# Python scripts are labelled as such

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {
  "profile.default_content_settings.popups": 0,
  "download.default_directory": os.getcwd(),
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True,
})
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--safebrowsing-disable-download-protection')
chrome_options.add_argument("test-type")

driver = webdriver.Chrome(options=chrome_options)

# ---------------------

# Loading the configuration files
with open("configs.json", "r") as file:
    configs = json.loads(file.read())

driver.get("https://urionlinejudge.com.br")
print("Loaded landing page")

# Login
elem = driver.find_element_by_name("email")
elem.send_keys(configs["email"])
sleep(0.5)

elem = driver.find_element_by_name("password")
elem.send_keys(configs["password"])
sleep(0.4)

elem = driver.find_element_by_xpath("//input[@value='Sign In']")
elem.click()

print("Signed In")

# Open the submissions page
elem = driver.find_element_by_xpath("//a[@href='/judge/pt/runs']")
elem.click()
sleep(0.35)

print("Listed all submissions")

# Filter only the accepted submissions
elem = driver.find_element_by_xpath("//option[@value='1']")
elem.click()
sleep(0.5)

elem = driver.find_element_by_xpath("//input[@value='Buscar']")
elem.click()

print("Filtered to accepted submissions")

# Iterate through accepted submissions pages
while True:
    # URL for the current submission page
    list_url = driver.current_url

    # Find all links to submissions in the table
    probs_row = driver.find_elements_by_xpath("//td[@class='id']//a")
    
    # Get all submission IDs and store them
    submission_ids = [i.text for i in probs_row] 
    for sub_id in submission_ids: # Iterate over the IDs
        driver.get("https://www.urionlinejudge.com.br/judge/pt/runs/code/" + sub_id) # Open submission

        # Get save-to-dropbox link
        link = driver.find_element_by_xpath("//div[@class='st-small-box']//a").get_attribute("href")
        
        # Open the dropbox link
        driver.get(link)
        sleep(0.5)
    
    driver.get(list_url) # Open the current submissions page
    # Get the next submission page URL
    href = driver.find_element_by_xpath("//a[contains(text(), 'Próximo')]").get_attribute("href").strip()

    # If it is not a valid URL, break the loop (Ugly)
    if len(href) < 5:
        break
    
    # Load the next submissions page
    driver.get(href)
    sleep(0.5)

print("Finished")
driver.close()

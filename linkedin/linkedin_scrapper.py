from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import yaml

####
from bs4 import BeautifulSoup
import urllib.parse
import os
import pandas as pd
import numpy as np

### Load credentials from the YAML file
with open("config.yml", 'r') as file:
    config = yaml.safe_load(file)

cr_username = config['credentials']['username']
cr_password = config['credentials']['password']

## Path, options and driver for Edge
PATH = os.getcwd() + "..\..\msedgedriver.exe"
service = Service(PATH)
op = webdriver.EdgeOptions()
op.add_argument('--ignore-certificate-errors')
op.add_argument('--incognito')

## Load selenium driver

driver = webdriver.Edge(service=service, options=op)
## Maximize browser
driver.maximize_window()

def linkedin_login(user_name, keyword):
    ## Browse page
    driver.get(f"https://www.linkedin.com/login")

    time.sleep(3)

    ### get username and password input boxes path
    username = driver.find_element(by=By.XPATH, value="//input[@name='session_key']")
    username.send_keys(user_name)
    time.sleep(3)

    password = driver.find_element(by=By.XPATH, value="//input[@name='session_password']")
    password.send_keys(keyword)
    time.sleep(3)
    ### click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    time.sleep(3)
    login_button.click()    

linkedin_login(cr_username,cr_password)
# driver.quit()
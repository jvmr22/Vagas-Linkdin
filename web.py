import os
import sys
import timeit
from datetime import datetime
from time import sleep

from openpyxl import load_workbook
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome = webdriver.Chrome("chromedriver", options=chrome_options)
chrome.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

chrome.find_element_by_id('username').send_keys('<>')
chrome.find_element_by_id('password').send_keys('<>')
chrome.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button').click()

WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.ID, 'extended-nav')))
chrome.find_element_by_xpath('//*[@id="ember32"]/input').click()
chrome.find_element_by_xpath('//*[@id="ember32"]/input').send_keys(Keys.ENTER)

WebDriverWait(chrome, 15).until(ec.visibility_of_element_located((By.CLASS_NAME, 'search-filters-bar__all-filters flex-shrink-zero mr3 artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view')))
chrome.find_element_by_xpath("//div[starts-with(@id, 'phone') and contains(@id, 'option')]").click()
chrome.find_element_by_class_name('search-filters-bar__all-filters flex-shrink-zero mr3 artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view').click()
'//*[@id="ember2816"]'
"//input[contains(@id, '-toDate')]"
'ember1284'
'ember241'
'ember260'
'ember241'
'ember734'
'ember1989'
'//*[@id="ember2837"]'


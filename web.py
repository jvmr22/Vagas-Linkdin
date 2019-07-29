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

WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-filters-bar__all-filters')))
chrome.find_element_by_class_name("search-filters-bar__all-filters").click()
WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.XPATH, '//*[@id="ember1017"]/input')))
chrome.find_element_by_id('ember708').send_keys('Universidade Federal do Ceará')

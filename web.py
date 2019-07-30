import os
from time import sleep

from selenium import webdriver
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
try:
    WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.ID, 'extended-nav')))
    chrome.find_element_by_xpath('//*[@id="ember32"]/input').click()
    chrome.find_element_by_xpath('//*[@id="ember32"]/input').send_keys(Keys.ENTER)
except:
    cod = input('Digite o codigo solicitado: ')
    #todo colocar o find_element para o a caixa do codigo
    pass

WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-filters-bar__all-filters')))
chrome.find_element_by_class_name("search-filters-bar__all-filters").click()

#  FILTROS
# Instituição de ensino
ies = 'Universidade Federal do Ceará'
WebDriverWait(chrome, 15).until(
    ec.presence_of_element_located((By.XPATH, "//input[@placeholder='Adicione uma instituição de ensino']")))
chrome.find_element_by_xpath("//input[@placeholder='Adicione uma instituição de ensino']") \
    .send_keys(ies)
sleep(1)
chrome.find_element_by_xpath("//input[@placeholder='Adicione uma instituição de ensino']").send_keys(Keys.ARROW_DOWN)
chrome.find_element_by_xpath("//input[@placeholder='Adicione uma instituição de ensino']").send_keys(Keys.ENTER)

# SETORES
# todo colocar um laço for pra varrer todos os filtros. Gerar planilha por filtro?
setores = ['Tecnologia da informação e serviços', 'Desenvolvimento de programas']  # , 'Software'
for setor in setores:
    chrome.find_element_by_xpath("//input[@placeholder='Adicione um setor']") \
        .send_keys(setor)
    sleep(1)
    chrome.find_element_by_xpath("//input[@placeholder='Adicione um setor']").send_keys(Keys.ARROW_DOWN)
    chrome.find_element_by_xpath("//input[@placeholder='Adicione um setor']").send_keys(Keys.ENTER)

sleep(1)
chrome.find_element_by_class_name('search-advanced-facets__button--apply').click()

# DIGITAR CARGOS
jobs = ['full stack', 'backend', 'Analista de sistemas', 'BI', 'Bussines Inteligence']
chrome.find_element_by_xpath('//*[@id="ember32"]/input').click()
chrome.find_element_by_xpath('//*[@id="ember32"]/input').send_keys(jobs[0])
chrome.find_element_by_xpath('//*[@id="ember32"]/input').send_keys(Keys.ENTER)

try:
    chrome.find_element_by_class_name('search-vertical-filter__filter-item-button').click()
except Exception as e:
    print(e)

WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-results__list')))
sleep(2)
people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
print('### {} pessoas ###'.format(len(people)))
index_person = 0

for i in range(0,len(people)):
    WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-result__info')))
    data = people[index_person].find_element_by_class_name('search-result__info').find_element_by_tag_name('a')
    print('nome: {}'.format(data.text.split('Conexão')[0]))
    data.click()
    WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'profile-background-image')))
    print('Visualização Perfil')
    sleep(5)
    chrome.back()

    WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-results__list')))
    people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
    index_person+=1


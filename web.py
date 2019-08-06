from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

profiles = []
keep_searching = True
max_page = 2
flag = 0

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
    # todo colocar o find_element para o a caixa do codigo
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

# LOCALIDADES
city = 'Fortaleza e Região, Brasil'
chrome.find_element_by_xpath("//input[@placeholder='Adicione uma localidade']").send_keys(city)
sleep(1)
chrome.find_element_by_xpath("//input[@placeholder='Adicione uma localidade']").send_keys(Keys.ARROW_DOWN)
chrome.find_element_by_xpath("//input[@placeholder='Adicione uma localidade']").send_keys(Keys.ENTER)

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

try:  # When has Linkdin Premium update sugestion
    chrome.find_element_by_class_name('search-paywall__warning-icon')
    people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
    print('### {} pessoas ###'.format(len(people) - 3))
    index_person = 3
except NoSuchElementException:
    people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
    print('### {} pessoas ###'.format(len(people)))
    index_person = 0

for page in range(1, max_page + 1):
    print('Pagina atual: {}'.format(page))

    for i in range(0, len(people)):
        if i >= 4:  # and (i<len(people)-1) : # scroll down page to load others profiles
            for s in range(i - 3):
                chrome.execute_script("window.scrollBy(0, 190)")
                sleep(1)

        WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-result__info')))
        try:
            data = people[index_person].find_element_by_class_name('search-result__info').find_element_by_tag_name('a')
        except:
            data = people[index_person].find_element_by_class_name('search-results__list').find_element_by_tag_name('a')

        name = data.text.split('Conexão')[0]
        # print('nome: {}'.format(data.text.split('Conexão')[0]))
        data.click()
        WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'profile-background-image')))
        print('{}º Visualização Perfil - {} '.format(i + 1, name))

        try:  # expand experiences
            print('Mostrando mais experiencias')
            chrome.find_element_by_class_name('pv-profile-section__see-more-inline').click()
            WebDriverWait(chrome, 15).until(
                ec.visibility_of_element_located((By.CLASS_NAME, 'pv-entity__position-group-pager')))
        except NoSuchElementException:
            pass

        chrome.execute_script("window.scrollTo(0,800);")
        WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'pv-profile-section-pager')))
        experiences = chrome.find_element_by_id('experience-section').find_elements_by_class_name(
            'pv-entity__position-group-pager')
        print('{} experiencias de trabalho'.format(len(experiences)))

        for work in experiences:
            try:
                chrome.find_element_by_class_name('pv-recent-activity-detail__header-container')
                chrome.back()
                WebDriverWait(chrome, 15).until(
                    ec.presence_of_element_located((By.CLASS_NAME, 'pv-profile-section-pager')))
            except:
                try:
                    job = work.find_element_by_tag_name('h3')
                    place = work.find_element_by_class_name('pv-entity__secondary-title')
                except:
                    chrome.execute_script("window.scrollBy(0, 190)")
                    try:
                        job = work.find_element_by_tag_name('h3')
                        place = work.find_element_by_class_name('pv-entity__secondary-title')
                    except:
                        place = work.find_element_by_tag_name('h3')
                        jobs = work.find_element_by_class_name('pv-entity__position-group').find_elements_by_tag_name(
                            'li')
                        for i in jobs:
                            flag = 1
                            job = i.find_element_by_tag_name('h3')
                            print('\t{} - {}'.format(job.text.split("\n", )[1], place.text.split("\n", )[1]))
                            print('---------')
            if flag == 0:
                print('\t{} - {}'.format(job.text, place.text))
            flag = 0
            profiles.append([name.split("\n", )[0], place.text, job.text])
            print('---------')

        chrome.back()
        WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-results__list')))
        people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
        index_person += 1

    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        chrome.find_element_by_class_name('artdeco-pagination__button--next').click()
        sleep(2)
        print('\t próxima pagina')
    except NoSuchElementException:
        # todo achar elemntos e clicar sempre no [2] segundo
        'artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view'
    WebDriverWait(chrome, 15).until(ec.presence_of_element_located((By.CLASS_NAME, 'search-result__info')))

    try:  # When has Linkdin Premium update sugestion
        chrome.find_element_by_class_name('search-paywall__warning-icon')
        people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
        print('### {} pessoas ###'.format(len(people) - 3))
        print('new people')
        index_person = 3
    except NoSuchElementException:
        people = chrome.find_element_by_class_name('search-results__list').find_elements_by_tag_name('li')
        print('### {} pessoas ###'.format(len(people)))
        print('new people 1')
        print(people)
        index_person = 0
print(profiles)
writer = pd.ExcelWriter('Vagas.xlsx', engine='xlsxwriter',
                        datetime_format='DD/MM/YYYY',
                        date_format='DD/MM/YYYY')
df_profiles = pd.DataFrame(profiles)
df_profiles.to_excel(writer)
writer.save()

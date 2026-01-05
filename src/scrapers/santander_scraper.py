from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import re
import ssl

options = Options()

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

countries = ["Notas de Prensa - México", "Notas de Prensa - Colombia", "Notas de Prensa - Chile",
              "Notas de Prensa - Argentina", "Notas de Prensa - Brasil", "Notas de Prensa - Uruguay"]

stop_date = datetime.strptime('01-01-2020', '%d-%m-%Y')
date_link = date.today()
first_time = True

control = 0
news_links = []
dates = []
titles = []
short_summary = []

while date_link > stop_date:
    if first_time:
        driver.get("https://www.santander.com/es/sala-de-comunicacion/notas-de-prensa")
        time.sleep(10)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        first_time = False
    
    links = driver.find_elements("class name", "filterable-results-total-result")

    for link in links:
        category = link.find_elements("class name", "filterable-results-total-result-category")[0].text
        date_link = link.find_elements("class name", "filterable-results-total-result-date")[0].text
        date_link = datetime.strptime(date_link, '%d-%m-%Y')
        if category in countries and date_link > stop_date:
            news_links.append(link.get_attribute("href"))
            dates.append(date_link)
            titles.append(link.find_elements("class name", "filterable-results-total-result-title")[0].text)
            short_summary.append(link.find_elements("class name", "filterable-results-total-result-text")[0].text)            
            
    next_page = driver.find_element("xpath", "//li[contains(@class, 'page-index next')]")
    next_page.click()
    time.sleep(10)
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

df = pd.DataFrame({
    'link': news_links,
    'title': titles,
    'date': dates,
    'summary': short_summary
})

df.to_csv('data/santander_news.csv', index=False, encoding='utf-8')

df = pd.read_csv("data/santander_news.csv")

paragraphs = []
review_summaries = []
k = 0

text_base = "Dicha cotización se muestra con una demora de hasta 15 minutos y en la hora local del mercado en el cual se muestra la cotización."

for site in df["link"]:
    url = requests.get(site).text
    page = BeautifulSoup(url, 'html.parser')   

    temp_summary = []
    
    span_tags_opening = page.find_all('span', {'class' : 'opening-entry'})
    span_tags_entradilla = page.find_all('span', {'class' : 'entradilla-risk-entry'})
    
    if span_tags_opening:
        span_tags = span_tags_opening
    elif span_tags_entradilla:
        span_tags = span_tags_entradilla
    else:
        temp_summary = ''
        
    if span_tags and temp_summary != '':
        for elem in span_tags_opening:
            temp_summary.append(elem.text.strip())
            
        if len(temp_summary) > 1:
            temp_summary = ' '.join(temp_summary)
        else:
            temp_summary = temp_summary[0]
        
    review_summaries.append(temp_summary)
    
    remove_elements = page.find_all(class_ = "opening-entry")
    for element in remove_elements:
        element.decompose()
    
    all_paragraphs = page.select('.cmp-text p p')
    
    for paragraph in all_paragraphs:
        text = paragraph.text.strip()
        text = text.replace('\xa0', ' ').strip()
        text = text.replace(text_base, '')
        text = re.sub(r'\s+', ' ', text).strip()
        if text != text_base and text != '' and text != df["title"][k] and df["summary"][k]:
            paragraphs.append(text)
            break

    #k += 1
    #if k > 10:
        #break

df["paragraph"] = paragraphs

df.to_csv('data/santander_news.csv', index=False, encoding='utf-8')














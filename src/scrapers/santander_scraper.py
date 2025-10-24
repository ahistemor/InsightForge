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
import ssl

options = Options()
# options.add_argument('--headless')  # Uncomment to run in headless mode

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





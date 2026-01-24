from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re

url = requests.get('https://www.baccredomatic.com/es-cr/nuestra-empresa/noticias?title=&sort_by=created').text

page = BeautifulSoup(url, 'html.parser')

news_pages = page.find_all('ul', {'class': 'pager__items js-pager__items'})[0].find_all('a')

page_num_list = []
titles = []
dates = []
links = []

for page in news_pages:
    page_url = 'https://www.baccredomatic.com/es-cr/nuestra-empresa/noticias' + page.get("href")
    page_num = re.search(r'page=(\d+)', page_url).group(1)
    page_num_list.append(page_num)
    
    if page_num == max(page_num_list):
        url = requests.get(page_url).text
        page = BeautifulSoup(url, 'html.parser')
        
        news_links = page.find_all('div', {'class': 'card-news__content'})
        
        for link in news_links:
            titles.append(link.find_all('h3')[0].text.strip())
            dates.append(link.find_all('span', {'class': 'card-news__value'})[0].text.strip())
            links.append('https://www.baccredomatic.com' + link.find_all('a', {'class': 'link link--arrow'})[0].get("href"))
    else:
        break



paragraphs = []

for link in df["link"]:
    url = requests.get(link).text
    page = BeautifulSoup(url, 'html.parser')
    page_paragraph = page.find_all('div', {'class': 'news__col-two'})[0].find_all('p')
    union_paragraph = []
    for paragraph in page_paragraph:
        text = paragraph.text.strip()
        if text != '':
            union_paragraph.append(text)
        if len(union_paragraph) > 4: #only 4 paragraphs are extracted
            break
    union_paragraph = ' '.join(union_paragraph)    
    paragraphs.append(union_paragraph)

df = pd.DataFrame({'link': links, 'title': titles, 'date': dates, 'paragraph': paragraphs})

df.to_csv('data/bac_news.csv', index=False, encoding='utf-8')







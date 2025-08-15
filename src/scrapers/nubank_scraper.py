from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

url = requests.get('https://international.nubank.com.br/es/files/').text

page = BeautifulSoup(url, 'html.parser')

news_links = page.find_all('a', {'class': 'files__content--card'})

list_links = []

for link in news_links:
    href = link.get("href")
    list_links.append(link["href"])

titles = []
dates = []
summaries = []
paragraphs = []

i = 1


for link in list_links:
    url = requests.get(link).text
    page = BeautifulSoup(url, 'html.parser')
    
    titles.append(page.find_all('h1', {'class' : 'heroSingle__content--title'})[0].text.strip())
    dates.append(page.find_all('div', {'class' : 'heroSingle__content--info'})[0].text.strip())
    summaries.append(page.find_all('p', {'class' : 'heroSingle__content--resume'})[0].text.strip())    
    paragraph = page.find('div', {'class' : 'singleBody__content'}).find_all('p')
    
    if not paragraph[0].text.strip():
        paragraphs.append(paragraph[1].text.strip())
    else:
        paragraphs.append(paragraph[0].text.strip())
    
    print(f"    Progress: {str(round((i/len(list_links))*100,0)) + '%'}", end="\r", flush=True)
    i += 1


df = pd.DataFrame({
    'link': list_links,
    'title': titles,
    'date': dates,
    'summary': summaries,
    'paragraph': paragraphs
})


df.to_csv('data/nubank_news.csv', index=False, encoding='utf-8')

